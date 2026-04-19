import os
import unittest
from unittest import mock

from app.services import notifications


class TestNotifications(unittest.TestCase):
    def setUp(self):
        # Ensure environment variables are set for tests
        self.env_patcher = mock.patch.dict(os.environ, {
            'TWILIO_ACCOUNT_SID': 'AC123',
            'TWILIO_AUTH_TOKEN': 'token123',
            'TWILIO_WHATSAPP_NUMBER': 'whatsapp:+1111111111',
            'EMAIL_USER': 'user@example.com',
            'EMAIL_PASS': 'pass123'
        })
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()

    @mock.patch('app.services.notifications.Client')
    def test_enviar_whatsapp_sends_message(self, mock_client_class):
        # Arrange
        mock_client = mock.Mock()
        mock_client.messages = mock.Mock()
        mock_client_class.return_value = mock_client

        telefono = '+1234567890'
        mensaje = 'Hola!'

        # Act
        notifications.enviar_whatsapp(telefono, mensaje)

        # Assert
        mock_client_class.assert_called_once_with('AC123', 'token123')
        mock_client.messages.create.assert_called_once_with(
            from_='whatsapp:+1111111111',
            body=mensaje,
            to=f'whatsapp:{telefono}'
        )

    @mock.patch('builtins.print')
    @mock.patch('app.services.notifications.Client')
    def test_enviar_whatsapp_handles_exception(self, mock_client_class, mock_print):
        # Arrange: messages.create raises
        mock_client = mock.Mock()
        mock_client.messages = mock.Mock()
        mock_client.messages.create.side_effect = Exception('twilio fail')
        mock_client_class.return_value = mock_client

        # Act: should not raise
        notifications.enviar_whatsapp('+123', 'msg')

        # Assert: print called with error message
        self.assertTrue(mock_print.called)
        called_args = mock_print.call_args[0][0]
        self.assertIn('Error WhatsApp:', called_args)

    @mock.patch('smtplib.SMTP')
    def test_enviar_correo_sends_email(self, mock_smtp_class):
        # Arrange: configure the context manager behavior
        mock_server = mock.Mock()
        mock_smtp = mock.Mock()
        mock_smtp.__enter__.return_value = mock_server
        mock_smtp_class.return_value = mock_smtp

        destinatario = 'dest@example.com'
        asunto = 'Prueba'
        cuerpo = 'Contenido del correo'

        # Act
        notifications.enviar_correo(destinatario, asunto, cuerpo)

        # Assert
        mock_smtp_class.assert_called_once_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('user@example.com', 'pass123')
        # Ensure send_message called with a message that has the expected headers
        self.assertTrue(mock_server.send_message.called)
        sent_msg = mock_server.send_message.call_args[0][0]
        self.assertEqual(sent_msg['Subject'], asunto)
        self.assertEqual(sent_msg['From'], 'user@example.com')
        self.assertEqual(sent_msg['To'], destinatario)

    @mock.patch('builtins.print')
    @mock.patch('smtplib.SMTP')
    def test_enviar_correo_handles_exception(self, mock_smtp_class, mock_print):
        # Arrange: using SMTP raises an exception when entering context
        mock_smtp = mock.Mock()
        mock_smtp.__enter__.side_effect = Exception('smtp fail')
        mock_smtp_class.return_value = mock_smtp

        # Act: should not raise
        notifications.enviar_correo('a@b.com', 'asunto', 'cuerpo')

        # Assert: print called indicating an email error
        self.assertTrue(mock_print.called)
        called_args = mock_print.call_args[0][0]
        self.assertIn('Error Email:', called_args)

    @mock.patch('smtplib.SMTP')
    def test_enviar_correo_sets_from_header_to_email_user(self, mock_smtp_class):
        # Arrange
        mock_server = mock.Mock()
        mock_smtp = mock.Mock()
        mock_smtp.__enter__.return_value = mock_server
        mock_smtp_class.return_value = mock_smtp

        # Act
        notifications.enviar_correo('x@y.com', 'AsuntoX', 'BodyX')

        # Assert header 'From' set to EMAIL_USER
        sent_msg = mock_server.send_message.call_args[0][0]
        self.assertEqual(sent_msg['From'], 'user@example.com')


if __name__ == '__main__':
    unittest.main()
