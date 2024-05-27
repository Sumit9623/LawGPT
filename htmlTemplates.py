css = '''
<style>
.chat-message {
    display:flex;
    gap:3%;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.2rem;
    color:white;
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063;
    margin-bottom:1rem;
}

.chat-message .message {
  width:90%;
  color: #fff;
}
.imagestyle{
    width:30px;
    height:30px;
    border-radius:50%;
}
'''

bot_template = '''
<div class="chat-message bot">
    <img src="https://as2.ftcdn.net/v2/jpg/01/37/89/95/1000_F_137899529_tDNYG6cKpxGzZ46SQeqrOIlg5VG5qKNa.jpg" class="imagestyle">
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user" >
    <img src="https://images.rawpixel.com/image_png_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIzLTAxL3JtNjA5LXNvbGlkaWNvbi13LTAwMi1wLnBuZw.png" class="imagestyle">
    <div class="message">{{MSG}}</div>
</div>
'''