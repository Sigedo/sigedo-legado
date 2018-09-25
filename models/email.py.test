import smtplib
 
# Credenciais
remetente    = 'seu-email@gmail.com'
senha        = 'sua-senha'
 
# Informações da mensagem
destinatario = 'email-do-destinatario@qualquercoisa.com'
assunto      = 'Enviando email com python'
texto        = 'Esse email foi enviado usando python! :)'
 
# Preparando a mensagem
msg = '\r\n'.join([
  'From: %s' % remetente,
  'To: %s' % destinatario,
  'Subject: %s' % assunto,
  '',
  '%s' % texto
  ])
 
# Enviando o email
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(remetente,senha)
server.sendmail(remetente, destinatario, msg)
server.quit()
