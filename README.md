# example-load-edi
## Step.1 ใช้คำสั่งเพื่อติดตั้ง package
<p>pip install -r requirements.txt</p>

## Step.2 สร้างไฟล์ .env
<p>คัดลอกตัวอย่างตามไฟล์ .env.example</p>
<p>API_PROD=False/True</p>
<p>API_HOST="https://218.225.124.157:9443/cehttp/servlet/MailboxServlet"</p>
<p>API_USERNAME==ชื่อผู้ใช้งาน</p>
<p>API_PASSWORD=รหัสผ่าน</p>
<p>LINE_NOTIFY_TOKEN=</p>
<p>SOURCE_DIR="data/download"</p>

## Step.3 รัน script
<p>รันที่ไฟล์ edi.py</p>

## หมายเหตุใช้กับ python3.9 ขึ้นไป
