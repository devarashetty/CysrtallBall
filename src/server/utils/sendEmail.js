import nodemailer from 'nodemailer';
import mg from 'nodemailer-mailgun-transport';

const auth = {
  auth: {
    api_key: 'key-d5d68f37b10da3c13aaa8d9234dc4480',
    domain: 'sandboxfca6c35d00d54a65a213dbbd619b06e6.mailgun.org'
  }
}
const sendEmail = async (recipient, url) => {
  console.log('-------------------------- sending mail--------------------', recipient, url);
  const transporter = nodemailer.createTransport(mg(auth));

  // send mail with defined transport object
  const info = await transporter.sendMail({
    from: 'marsai493@gmail.com', // sender address
    to: 'monicabedi493@gmail.com',
    subject: 'Hello ✔', // Subject line
    text: 'Hello world?', // plain text body
    html: `<html>
      <body>
        <b>Hello world? </b>
        <a href="${url}">Click to Test!</a>
      </body>
    </html>` // html body
  });

  console.log('Message sent: %s', info.messageId);
  // Message sent: <b658f8ca-6296-ccf4-8306-87d57a0b4321@example.com>

  // Preview only available when sending through an Ethereal account
  console.log('Preview URL: %s', nodemailer.getTestMessageUrl(info));
  // Preview URL: https://ethereal.email/message/WaQKMgKddxQDoou...
};


export default sendEmail;