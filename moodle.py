from robobrowser import RoboBrowser
import requests
import os
    
site_url = "http://gyan.fragnel.edu.in:2222/moodle/login/index.php"
userid =input("enter your roll no")
password =input("enter your moodle password")
br=RoboBrowser(parser='html.parser')
s = requests.Session()
s.get(site_url)
s.post(site_url, data={'username': userid, 'password': password})
br.open(site_url)
form=br.get_form()
form['username'].value=userid
form['password'].value=password
br.submit_form(form)
trial=br.find("div",{"class":"logininfo"})
if len(trial.find_all('a'))==2:
    print("Successfully Logged In")
else:
    print("Login Failed")
navigate_to_base=br.find("p",{"class":"tree_item leaf hasicon"})
base_url=navigate_to_base.a['href']
br.open(base_url)
#all code above remains same
root="moodle"
if not os.path.exists(root):
    os.mkdir(root)
subjects=['Internet Programming','MEP','Cryptography and Network Security','ADMT']

for Subject in subjects:
    new_files=[]
    if not os.path.exists(root+'/'+Subject):
        os.mkdir(root+'/'+Subject)
    br.open(base_url)
    c=br.find("a",{"title":Subject})
    var=c['href']
    br.open(var)
    l=br.find_all("div",{"class":"activityinstance"})
    news_forum="http://gyan.fragnel.edu.in:2222/moodle/mod/forum/view.php?id=8384"
    pdf="http://gyan.fragnel.edu.in:2222/moodle/theme/image.php/formfactor/core/1453110796/f/pdf-24"
    docx="http://gyan.fragnel.edu.in:2222/moodle/theme/image.php/formfactor/core/1453110796/f/document-24"
    ppt="http://gyan.fragnel.edu.in:2222/moodle/theme/image.php/formfactor/core/1453110796/f/powerpoint-24"
    txt="http://gyan.fragnel.edu.in:2222/moodle/theme/image.php/formfactor/core/1453110796/f/text-24"
    archive="http://gyan.fragnel.edu.in:2222/moodle/theme/image.php/formfactor/core/1453110796/f/archive-24"
    s_code="http://gyan.fragnel.edu.in:2222/moodle/theme/image.php/formfactor/core/1453110796/f/sourcecode-24"
    folder="http://gyan.fragnel.edu.in:2222/moodle/theme/image.php/formfactor/folder/1453110796/icon"
    survey="http://gyan.fragnel.edu.in:2222/moodle/theme/image.php/formfactor/feedback/1453110796/icon"
    links=[]
    folder_links=[]
    new_files=[]
    for i in l:
        if i.a.img['src']==news_forum or i.a.img['src']==survey :
            continue
        elif i.a.img['src']==pdf:
            br.open(i.a['href'])
            temp=br.find(id="resourceobject")
            if(temp==None):
                br.open(i.a['href'])
                links.append(br.url)
                continue
            pdf_link=temp['data']
            links.append(pdf_link)
        elif i.a.img['src']==docx or i.a.img['src']==ppt or i.a.img['src']==txt or i.a.img['src']==archive or i.a.img['src']==s_code:
            br.open(i.a['href'])
            links.append(br.url)
        elif i.a.img['src']==folder:
            if not os.path.exists(root+'/'+Subject+'/'+i.span.text):
                    os.mkdir(root+'/'+Subject+'/'+i.span.text)
            folder_links.append(i.a['href'])
            br.open(i.a['href'])
            dox=br.find_all("span",{"class":"fp-filename-icon"})
            for j in dox:
                file_url=j.a['href']
                r = s.get(file_url)
                o_file=file_url[file_url.find('/0/')+3:-16:1]
                if not os.path.exists(root+'/'+Subject+'/'+i.span.text+'/'+o_file):
                    new_files.append(o_file)
                    with open(root+'/'+Subject+'/'+i.span.text+'/'+o_file, 'wb') as output:
                        output.write(r.content)
                    print(f"requests:: File {o_file} downloaded successfully!")
                
    #print(links)
    #print(len(links))

    for file_url in links:
        r = s.get(file_url)
        if(file_url.find('forcedownload=1')==-1):
            o_file=file_url[file_url.rfind('/')+1:]
        else:
            o_file=file_url[file_url.rfind('/')+1:-16:1]
        if not os.path.exists(root+'/'+Subject+'/'+o_file):
            new_files.append(o_file)
            with open(root+'/'+Subject+'/'+o_file, 'wb') as output:
                output.write(r.content)
            print(f"requests:: File {o_file} downloaded successfully!")
    s.close()
    if(len(new_files)>1):
        print(str(len(new_files))+" new files have been downloaded succesfully")
    elif (len(new_files)==0):
        print("No new files have been uploaded")
    else:
          print(new_files[0]+"has been downloaded successfully")  #desktop-notification new_file is list of files
