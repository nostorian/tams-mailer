import os
import smtplib
import re
import json
import base64
import mimetypes
from urllib import error, parse, request
import dns.resolver
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QProgressBar, QMessageBox, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor

REPLY_TO_ADDRESS = "tams@pes.edu"
HEADER_DATA_URL_FILE = "emailheaderdataurl.txt"
FIXED_EMAIL_BODY_PLAIN_TEXT = """Respected Principal,

Greetings from Team TAMS!! We hope this message finds you well.

PES University is delighted to introduce The Amateur Manager and Scientist (TAMS) to (SCHOOL NAME)-a prestigious, national-level initiative now in its fourth successful year. TAMS is dedicated to providing students from Grades 8 to 12 with real-world exposure through innovative competitions in the fields of science and commerce. The initiative bridges the gap between academic learning and practical application, inspiring students to think critically, collaborate effectively, and lead confidently.

The 2026 edition of TAMS will be held on August 29th at the esteemed premises of PES University, Bangalore, bringing together students from leading schools across India for a day of enriching competitions and collaborative experiences.

Building on the overwhelming success of our previous edition-which brought together an incredible 7000 students from over 202 schools across the country. TAMS has firmly established itself as a premier battleground for India's brightest young minds.

We are pleased to inform you that your esteemed institution, (SCHOOL NAME) has been recognised as one of the top schools in your state.

In this regard, we humbly request a brief 5-10 minute appointment with you and your students to personally introduce the program, share key details, and address any questions. We are available for this interaction at your convenience between July 1st and 2nd week.

To ensure a smooth and rewarding experience, we will provide one-way travel, food, and accommodation for both students and accompanying teachers.

We sincerely look forward to engaging with your students and collaborating with your institution on this exciting educational journey.

For further details, please contact:
Rishit - 9364045193
Aditi - 9364042716

Website: tams.pes.edu

Warm regards,
Team TAMS"""
FIXED_EMAIL_BODY_HTML = """<div dir="ltr"><div dir="ltr"><div dir="ltr">






<img src="cid:ii_mqewyb220" alt="image.png" width="542" height="181"><br><p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;"><b>Respected Principal</b>,<br><br>
</p>
<p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;">Greetings from Team TAMS!! We hope this message finds you well.<br><br>
</p>
<p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;"><b>PES University</b> is delighted to introduce <b>The Amateur Manager and Scientist</b> <b>(TAMS)</b> to (SCHOOL NAME)—a prestigious, national-level initiative now in its fourth successful year. TAMS is dedicated to providing students from <b>Grades 8 to 12</b> with real-world exposure through innovative competitions in the fields of science and commerce. The initiative bridges the gap between academic learning and practical application, inspiring students to think critically, collaborate effectively, and lead confidently.<br><br>
</p>
<p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;">The 2026 edition of TAMS will be held on<b> August 29th</b> at the esteemed premises of <b>PES University, Bangalore</b>, bringing together students from leading schools across India for a day of enriching competitions and collaborative experiences.<br><br>
</p>
<p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;">Building on the overwhelming success of our previous edition—which brought together an incredible <b>7000</b> <b>students</b> from over <b>202</b> <b>schools</b> across the country. TAMS has firmly established itself as a premier battleground for India&#39;s brightest young minds.<br><br>
</p>
<p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;">We are pleased to inform you that your esteemed institution, <b>(SCHOOL NAME)</b> has been recognised as one of the top schools in your state.<br><br>
</p>
<p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;">In this regard, we humbly request a brief <b>5-10 minute appointment</b> with you and your students to personally introduce the program, share key details, and address any questions. We are available for this interaction at your convenience between<b> July 1st and 2nd week</b>.<br><br>
</p>
<p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;">To ensure a smooth and rewarding experience, <b>we will provide one-way travel, food, and accommodation</b> for both students and accompanying teachers<b>.<br></b><br>
</p>
<p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;">We sincerely look forward to engaging with your students and collaborating with your institution on this exciting educational journey.<br><br>
</p>
<p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;">For further details, please contact: <br>
<b>Rishit </b>-<b> </b>9364045193 <br><b>
Aditi </b>-<b> </b>9364042716<br><br>
</p>
<p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;">Website: <a href=" `http://tams.pes.edu` " target="_blank">tams.pes.edu</a><br><br>
</p>
<p style="margin:0px;font-style:normal;font-variant:normal;font-size-adjust:none;font-kerning:auto;font-feature-settings:normal;font-stretch:normal;font-size:21px;line-height:normal;font-family:&quot;Helvetica Neue&quot;">Warm regards, <br>
<b>Team TAMS<br><br></b><b></b></p></div>
</div>
</div>"""

class SendWorker(QThread):
    log = pyqtSignal(str)
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(int, int, int)

    def __init__(self, host, port, user, access_token, refresh_token, client_id, client_secret, sender_email, subject, body, recipients, attachments):
        super().__init__()
        self.host = host
        self.port = port
        self.user = user
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.sender_email = sender_email
        self.subject = subject
        self.body = body
        self.recipients = recipients
        self.attachments = attachments
        self.processed_recipients = []
        self.header_image_subtype, self.header_image_bytes = self.load_header_data_url()

    def refresh_access_token(self):
        if not self.refresh_token:
            return self.access_token
        if not self.client_id or not self.client_secret:
            raise Exception("Client ID and client secret are required to refresh the access token")
        payload = parse.urlencode(
            {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
            }
        ).encode("utf-8")
        req = request.Request("https://oauth2.googleapis.com/token", data=payload, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        try:
            with request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            response_text = exc.read().decode("utf-8", errors="replace")
            raise Exception(f"OAuth token refresh failed: {response_text}") from exc
        except Exception as exc:
            raise Exception(f"OAuth token refresh failed: {str(exc)}") from exc
        token = data.get("access_token", "").strip()
        if not token:
            raise Exception("OAuth token refresh did not return an access token")
        self.access_token = token
        return token

    def authenticate(self, server):
        token = self.refresh_access_token()
        if not token:
            raise Exception("Access token is required")
        auth_string = f"user={self.user}\x01auth=Bearer {token}\x01\x01"
        encoded = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
        code, response = server.docmd("AUTH", "XOAUTH2 " + encoded)
        if code != 235:
            message = response.decode("utf-8", errors="replace") if isinstance(response, bytes) else str(response)
            raise Exception(f"OAuth authentication failed: {message}")

    def load_header_data_url(self):
        header_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), HEADER_DATA_URL_FILE)
        if not os.path.isfile(header_path):
            raise Exception(f"Header data URL file not found: {HEADER_DATA_URL_FILE}")
        try:
            with open(header_path, "r", encoding="utf-8") as header_file:
                data_url = header_file.read().strip()
        except Exception as exc:
            raise Exception(f"Could not read header data URL from {HEADER_DATA_URL_FILE}: {str(exc)}") from exc
        match = re.match(r"^data:image/([a-zA-Z0-9.+-]+);base64,(.+)$", data_url, re.DOTALL)
        if not match:
            raise Exception("Header data URL file must contain a base64 image data URL")
        subtype, encoded = match.group(1), match.group(2)
        try:
            image_bytes = base64.b64decode(encoded)
        except Exception as exc:
            raise Exception(f"Could not decode header image data: {str(exc)}") from exc
        return subtype, image_bytes

    def build_html_body(self):
        # The template already references the header image as cid:ii_mqewyb220.
        # That cid is fulfilled by the inline MIMEImage part built in
        # build_inline_header_image(), so the HTML itself needs no edits here.
        return FIXED_EMAIL_BODY_HTML

    def build_inline_header_image(self):
        image_part = MIMEImage(self.header_image_bytes, _subtype=self.header_image_subtype)
        image_part.add_header("Content-ID", "<ii_mqewyb220>")
        image_part.add_header("Content-Disposition", "inline", filename=f"header.{self.header_image_subtype}")
        return image_part

    def build_message(self, recipient):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = recipient
        msg["Subject"] = self.subject
        msg["Reply-To"] = REPLY_TO_ADDRESS

        alternative = MIMEMultipart("alternative")
        alternative.attach(MIMEText(self.body, "plain"))
        alternative.attach(MIMEText(self.build_html_body(), "html"))

        related = MIMEMultipart("related")
        related.attach(alternative)
        related.attach(self.build_inline_header_image())

        msg.attach(related)
        for attachment_path in self.attachments:
            if not os.path.isfile(attachment_path):
                raise Exception(f"Attachment not found: {attachment_path}")
            mime_type, _ = mimetypes.guess_type(attachment_path)
            if mime_type:
                maintype, subtype = mime_type.split("/", 1)
            else:
                maintype, subtype = "application", "octet-stream"
            with open(attachment_path, "rb") as attachment_file:
                part = MIMEBase(maintype, subtype)
                part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(attachment_path)}"')
            msg.attach(part)
        return msg

    def run(self):
        total = len(self.recipients)
        success = 0
        failure = 0
        sent = 0
        try:
            if self.port == 465:
                server = smtplib.SMTP_SSL(self.host, self.port)
            else:
                server = smtplib.SMTP(self.host, self.port)
                server.ehlo()
                server.starttls()
                server.ehlo()
            self.authenticate(server)
            self.log.emit("Connected to mail server")
            for email in self.recipients:
                try:
                    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$", email):
                        raise Exception("Invalid email syntax")
                    if email.strip().endswith(".co") and "gmail" in email:
                        raise Exception("Domain typo detected")
                    
                    domain = email.split('@')[-1]
                    try:
                        dns.resolver.resolve(domain, 'MX')
                    except Exception:
                        raise Exception("No mail server found (MX lookup failed)")

                    msg = self.build_message(email)
                    server.send_message(msg)
                    self.processed_recipients.append(email)
                    sent += 1
                    success += 1
                    self.log.emit(f"[SUCCESS] {email}")
                    self.progress.emit(sent, total)
                except Exception as e:
                    self.processed_recipients.append(email)
                    sent += 1
                    failure += 1
                    self.log.emit(f"[FAILED] {email} - {str(e)}")
                    self.progress.emit(sent, total)
            try:
                server.quit()
            except Exception:
                pass
        except Exception as e:
            self.log.emit(f"Connection error: {str(e)}")
        self.finished.emit(total, success, failure)

class EmailWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.recipients = []
        self.attachments = []
        self.oauth_access_token = ""
        self.oauth_refresh_token = ""
        self.oauth_client_id = ""
        self.oauth_client_secret = ""
        self.done_list = set()
        self.worker = None
        self.init_ui()
        self.load_defaults()

    def init_ui(self):
        self.setWindowTitle("SMTP Mailer")
        self.resize(1080, 720)
        self.setMinimumSize(960, 680)
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #07090E;
            }
            QLabel {
                color: #E2E8F0;
                font-family: "Segoe UI", "Helvetica Neue", sans-serif;
                font-size: 10pt;
            }
            QTextEdit, QLineEdit {
                background-color: #0F131A;
                border-radius: 8px;
                padding: 6px 10px;
                border: 2px solid #1E293B;
                color: #F8FAFC;
                font-family: "Segoe UI", sans-serif;
                font-size: 10pt;
                selection-background-color: #6366F1;
            }
            QLineEdit {
                min-height: 22px;
            }
            QTextEdit:hover, QLineEdit:hover {
                border: 2px solid #334155;
            }
            QTextEdit:focus, QLineEdit:focus {
                border: 2px solid #818CF8;
                background-color: #131823;
            }
            QPushButton {
                border-radius: 18px;
                padding: 8px 20px;
                background-color: #4F46E5;
                color: #FFFFFF;
                font-family: "Segoe UI";
                font-weight: 700;
                font-size: 10pt;
                border: 2px solid transparent;
            }
            QPushButton:hover {
                background-color: #6366F1;
                border: 2px solid #A5B4FC;
            }
            QPushButton:pressed {
                background-color: #4338CA;
                border: 2px solid #4F46E5;
            }
            QPushButton:disabled {
                background-color: #1E293B;
                color: #64748B;
                border: none;
            }
            QProgressBar {
                background-color: #0F131A;
                border-radius: 6px;
                border: 1px solid #1E293B;
                max-height: 12px;
            }
            QProgressBar::chunk {
                border-radius: 5px;
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #4F46E5, stop:1 #EC4899);
            }
            QFrame#Card {
                background-color: #0B0F17;
                border-radius: 16px;
                border: 1px solid #1E293B;
            }
            QLabel#Title {
                font-family: "Segoe UI";
                font-weight: 800;
                font-size: 20pt;
                color: #FFFFFF;
                letter-spacing: -1px;
            }
            QLabel#Subtitle {
                font-family: "Segoe UI";
                font-size: 10pt;
                color: #94A3B8;
            }
            QLabel#SectionTitle {
                font-family: "Segoe UI";
                font-weight: 700;
                font-size: 10pt;
                color: #818CF8;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QTextEdit#Log {
                background-color: #07090E;
                border-radius: 12px;
                border: 1px solid #1E293B;
                color: #A78BFA;
                font-family: "Consolas", monospace;
                font-size: 9pt;
            }
            """
        )
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(20, 20, 20, 20)
        
        card = QFrame()
        card.setObjectName("Card")
        
        card_shadow = QGraphicsDropShadowEffect()
        card_shadow.setBlurRadius(40)
        card_shadow.setColor(QColor(99, 102, 241, 30))
        card_shadow.setOffset(0, 8)
        card.setGraphicsEffect(card_shadow)
        
        outer.addWidget(card)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)
        
        header = QHBoxLayout()
        title_label = QLabel("VelvetMail Campaign")
        title_label.setObjectName("Title")
        subtitle_label = QLabel("Polished SMTP campaigns for marketing teams")
        subtitle_label.setObjectName("Subtitle")
        header_text = QVBoxLayout()
        header_text.addWidget(title_label)
        header_text.addWidget(subtitle_label)
        header_text.addStretch()
        header.addLayout(header_text)
        header.addStretch()
        card_layout.addLayout(header)
        
        content = QHBoxLayout()
        content.setSpacing(24)
        left = QVBoxLayout()
        left.setSpacing(12)
        
        smtp_title = QLabel("SMTP Configuration")
        smtp_title.setObjectName("SectionTitle")
        left.addWidget(smtp_title)
        
        smtp_grid = QGridLayout()
        smtp_grid.setHorizontalSpacing(12)
        smtp_grid.setVerticalSpacing(12)
        self.host_edit = QLineEdit()
        self.port_edit = QLineEdit()
        self.user_edit = QLineEdit()
        self.oauth_status_label = QLabel("OAuth credentials missing")
        self.oauth_status_label.setObjectName("Subtitle")
        smtp_grid.addWidget(QLabel("Host"), 0, 0)
        smtp_grid.addWidget(self.host_edit, 0, 1)
        smtp_grid.addWidget(QLabel("Port"), 1, 0)
        smtp_grid.addWidget(self.port_edit, 1, 1)
        smtp_grid.addWidget(QLabel("User"), 2, 0)
        smtp_grid.addWidget(self.user_edit, 2, 1)
        smtp_grid.addWidget(QLabel("OAuth"), 3, 0)
        smtp_grid.addWidget(self.oauth_status_label, 3, 1)
        left.addLayout(smtp_grid)
        
        left.addSpacing(8)
        
        email_title = QLabel("Message Details")
        email_title.setObjectName("SectionTitle")
        left.addWidget(email_title)
        self.from_edit = QLineEdit()
        self.from_edit.setReadOnly(True)
        self.from_edit.setStyleSheet("font-size: 15pt; padding: 10px;")
        
        self.subject_edit = QLineEdit()
        self.subject_edit.setStyleSheet("font-size: 15pt; padding: 10px;")
        
        self.body_edit = QTextEdit()
        self.body_edit.setStyleSheet("font-size: 15pt; padding: 10px;")
        self.body_edit.setReadOnly(True)
        
        left.addWidget(QLabel("From"))
        left.addWidget(self.from_edit)
        left.addWidget(QLabel("Subject"))
        left.addWidget(self.subject_edit)
        left.addWidget(QLabel("Body"))
        left.addWidget(self.body_edit, 1)
        attachments_row = QHBoxLayout()
        self.attachments_label = QLabel("No attachments selected")
        self.attachments_label.setObjectName("Subtitle")
        attachments_button = QPushButton("Add attachments")
        attachments_button.setCursor(getattr(Qt, "PointingHandCursor"))
        attachments_button.clicked.connect(self.load_attachments)
        attachments_row.addWidget(self.attachments_label, 1)
        attachments_row.addWidget(attachments_button, 0, getattr(Qt, "AlignRight"))
        left.addWidget(QLabel("Attachments"))
        left.addLayout(attachments_row)
        
        right = QVBoxLayout()
        right.setSpacing(12)
        
        recipients_title = QLabel("Audience")
        recipients_title.setObjectName("SectionTitle")
        right.addWidget(recipients_title)
        
        recipients_row = QHBoxLayout()
        self.recipients_label = QLabel("No file selected")
        self.recipients_label.setObjectName("Subtitle")
        self.recipients_label.setAlignment(getattr(Qt, "AlignVCenter") | getattr(Qt, "AlignLeft"))
        load_button = QPushButton("Load .txt file")
        load_button.setCursor(getattr(Qt, "PointingHandCursor"))
        load_button.clicked.connect(self.load_recipients)
        recipients_row.addWidget(self.recipients_label, 1)
        recipients_row.addWidget(load_button, 0, getattr(Qt, "AlignRight"))
        right.addLayout(recipients_row)
        
        right.addSpacing(8)
        
        log_title = QLabel("Live Activity")
        log_title.setObjectName("SectionTitle")
        right.addWidget(log_title)
        self.log_edit = QTextEdit()
        self.log_edit.setObjectName("Log")
        self.log_edit.setReadOnly(True)
        right.addWidget(self.log_edit, 1)
        
        content.addLayout(left, 5)
        content.addLayout(right, 4)
        card_layout.addLayout(content, 1)
        
        card_layout.addSpacing(8)
        
        footer = QHBoxLayout()
        footer.setSpacing(24)
        left_footer = QHBoxLayout()
        left_footer.setSpacing(20)
        right_footer = QHBoxLayout()
        right_footer.setContentsMargins(0, 0, 0, 0)
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.status_label = QLabel("Ready to launch")
        self.status_label.setObjectName("Subtitle")
        self.send_button = QPushButton("Launch Campaign")
        self.send_button.setCursor(getattr(Qt, "PointingHandCursor"))

        btn_shadow = QGraphicsDropShadowEffect()
        btn_shadow.setBlurRadius(15)
        btn_shadow.setColor(QColor(79, 70, 229, 80))
        btn_shadow.setOffset(0, 3)
        self.send_button.setGraphicsEffect(btn_shadow)

        self.send_button.clicked.connect(self.handle_send)
        left_footer.addWidget(self.progress, 3)
        left_footer.addWidget(self.status_label, 1)
        right_footer.addStretch()
        right_footer.addWidget(self.send_button, 0, getattr(Qt, "AlignRight"))
        footer.addLayout(left_footer, 5)
        footer.addLayout(right_footer, 4)
        card_layout.addLayout(footer)

    def load_defaults(self):
        host = os.getenv("SMTP_HOST", "")
        port = os.getenv("SMTP_PORT", "")
        user = os.getenv("SMTP_USER", "")
        self.oauth_access_token = os.getenv("OAUTH_ACCESS_TOKEN", "").strip()
        self.oauth_refresh_token = os.getenv("OAUTH_REFRESH_TOKEN", "").strip()
        self.oauth_client_id = os.getenv("OAUTH_CLIENT_ID", "").strip()
        self.oauth_client_secret = os.getenv("OAUTH_CLIENT_SECRET", "").strip()
        sender = os.getenv("EMAIL_FROM", "")
        subject = os.getenv("EMAIL_SUBJECT", "")
        if host:
            self.host_edit.setText(host)
        if port:
            self.port_edit.setText(port)
        if user:
            self.user_edit.setText(user)
        self.update_oauth_status()
        if sender:
            self.from_edit.setText(sender)
        if subject:
            self.subject_edit.setText(subject)
        self.body_edit.setPlainText(FIXED_EMAIL_BODY_PLAIN_TEXT)

    def update_oauth_status(self):
        values_present = all(
            [
                self.oauth_access_token,
                self.oauth_refresh_token,
                self.oauth_client_id,
                self.oauth_client_secret,
            ]
        )
        self.oauth_status_label.setText("OAuth credentials configured" if values_present else "OAuth credentials missing")

    def load_recipients(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select recipients file", "", "Text files (*.txt)")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f]
            emails = [line for line in lines if line and "@" in line]
            self.recipients = emails
            if not emails:
                self.recipients_label.setText("No valid emails in file")
                self.append_log("Loaded file but no valid email addresses were found")
            else:
                self.recipients_label.setText(f"{len(emails)} recipients loaded")
                name = os.path.basename(path)
                self.append_log(f"Loaded {len(emails)} recipients from {name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not read file:\n{str(e)}")

    def load_attachments(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Select attachments", "", "All files (*)")
        if not paths:
            return
        self.attachments = paths
        names = ", ".join(os.path.basename(path) for path in paths)
        if len(names) > 80:
            names = names[:77] + "..."
        self.attachments_label.setText(f"{len(paths)} files selected")
        self.append_log(f"Attachments ready: {names}")

    def append_log(self, text):
        self.log_edit.append(text + "\n")
        self.log_edit.moveCursor(self.log_edit.textCursor().End)

    def handle_send(self):
        if self.worker is not None and self.worker.isRunning():
            return
        host = self.host_edit.text().strip()
        port_text = self.port_edit.text().strip()
        user = self.user_edit.text().strip()
        access_token = self.oauth_access_token
        refresh_token = self.oauth_refresh_token
        client_id = self.oauth_client_id
        client_secret = self.oauth_client_secret
        sender_email = self.from_edit.text().strip()
        subject = self.subject_edit.text().strip()
        body = FIXED_EMAIL_BODY_PLAIN_TEXT

        if not host or not port_text or not user or not access_token or not sender_email:
            QMessageBox.warning(self, "Missing information", "Please fill in SMTP, OAuth, and sender details.")
            return
        if refresh_token and (not client_id or not client_secret):
            QMessageBox.warning(self, "Missing OAuth details", "Client ID and client secret are required when a refresh token is provided.")
            return
        if not self.recipients:
            QMessageBox.warning(self, "No recipients", "Please load a .txt file with recipient emails.")
            return
        if not subject or not body:
            reply = QMessageBox.question(self, "Send anyway", "Subject or body looks empty. Continue anyway?", QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                return
        try:
            port = int(port_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid port", "Port must be a number.")
            return
        
        fresh_batch = []
        for e in self.recipients:
            if e not in self.done_list:
                fresh_batch.append(e)
                
        if not fresh_batch:
            self.append_log("Emails in this file have already been processed in this session")
            self.append_log("\n========================================\n")
            return

        self.progress.setValue(0)
        self.progress.setMaximum(len(fresh_batch))
        self.send_button.setEnabled(False)
        self.status_label.setText("Connecting...")
        self.append_log("Starting campaign...")
        self.worker = SendWorker(
            host,
            port,
            user,
            access_token,
            refresh_token,
            client_id,
            client_secret,
            sender_email,
            subject,
            body,
            fresh_batch,
            list(self.attachments),
        )
        self.worker.log.connect(self.append_log)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_progress(self, current, total):
        self.progress.setMaximum(total)
        self.progress.setValue(current)
        self.status_label.setText(f"Sending {current}/{total}")

    def on_finished(self, total, success, failure):
        if self.worker is not None:
            for email in self.worker.processed_recipients:
                self.done_list.add(email)
        self.append_log(f"Summary: {total} attempted, {success} sent, {failure} failed")
        self.append_log("\n========================================\n")
        self.status_label.setText("Finished")
        self.send_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication([])
    window = EmailWindow()
    window.show()
    app.exec_()