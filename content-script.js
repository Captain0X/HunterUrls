inject_code = `
var button = document.getElementById("spider_on_off_botton");
button.addEventListener("click", () =>
  spider_urls()
, false);
function cros_req(parameter){
    spider_iframe=document.getElementById("spider_iframe")
    //利用iframe标签发起跨域请求,把获取到的url发给客户端,为了降低数据保存服务的请求处理压力，每次请求创建一个不显示的iframe标签
    var css_tag = document.createElement("iframe");
    css_tag.setAttribute('src', 'http://127.0.0.1:12587/save_api?data_base64='+btoa(JSON.stringify(parameter)));
    css_tag.setAttribute("id","spider_iframe");
    css_tag.setAttribute('style','display:none;');
    document.body.appendChild(css_tag)
    


}
function spider_urls(){
 console.log("%c------%cHunterUrls%c------",'color: #0D6EFD','background: #0D6EFD; color: #FFFFFF','color: #0D6EFD');
var urls=[];window.$$=document.querySelectorAll.bind(document),$$('*').forEach(element => {
    //黑名单正则表达式
    denyList=new RegExp('127\.0\.0\.1|\.css|\.ppt|\.jpg|\.odm|\.odg|\.svg|\.xls|\.ods|\.jpeg|\.mp4|\.tar|\.xlsx|\.mpeg|\.wma|\.odt|\.rar|\.bmp|\.odb|\.mp3|\.pdf|\.docx|\.avi|\.wav|\.aac|\.png|\.flac|\.7z|\.wmv|\.mov|\.pptx|\.odf|\.iso|\.zip|\.doc|\.webm|\.gif|\.csv|\.ogg|\.odp|\.rtf|\.odc|\.mpg|\.mkv');
    if (typeof element.src=='string' && element.src.indexOf('http')==0 && denyList.exec(element.src)===null){
        urls.push(element.src)
    }
    if (typeof element.href=='string'&& element.href.indexOf('http')==0 && denyList.exec(element.href)===null){
        urls.push(element.href)
    }
    if (typeof element.url=='string'&& element.url.indexOf('http')==0 && denyList.exec(element.url)===null){
        urls.push(element.href)
    }
    //限制发送url的数量
    if (urls.length>20){
        hostname=document.location.href;
        url_dict={};
        url_dict[hostname]=urls;
        
        console.log(urls);
        cros_req(url_dict)
        //置空变量
        urls=[]

    }
});
if (urls.length>0){

    hostname=document.location.href;
    url_dict={};
    url_dict[hostname]=urls;
    
    console.log(urls);
    cros_req(url_dict)
    urls=[];
}

}`;

var button_tag_style = document.createElement("style");
button_tag_style.innerHTML = `
:root{
  --spider-color: royalblue;
}
.spider_on_off_botton_float {
    width: 130px;
    height: 50px;
    position: fixed;
    bottom: 50px;
    right: 50px;
    z-index: 901;
    }
 
.spider_on_off_float_btn{

  color: #000000d9;
  border: 2px solid #d9d9d9;
  background-color: transparent;
  border-radius: 6px;
  box-shadow: 0 2px #00000004;
  cursor: pointer;
  transition: .3s;
   padding: 0.5rem 1rem;
	font-size: 1.3em;
	font-weight: 1.5em;
	color: #899DBB;
	text-align: center;
	text-decoration: none;
	vertical-align: middle;
	cursor: pointer;
}
.spider_on_off_float_btn:hover{
  color: var(--spider-color);
  border-color: currentColor;
}
  `;
document.body.appendChild(button_tag_style);



{/* <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'"> */}

var button_tag = document.createElement("button");
button_tag.setAttribute('id', 'spider_on_off_botton')
button_tag.setAttribute('type', 'button')
button_tag.setAttribute("class", "spider_on_off_botton_float spider_on_off_float_btn")
button_tag.innerHTML = '爬取链接';
document.body.appendChild(button_tag);
var script = document.createElement("script");
script.setAttribute('type', 'text/javascript')
script.appendChild(document.createTextNode(inject_code));
document.body.appendChild(script);
