# compressor-for-discord
 A Simple to use all in one media compressor for Discord
 Only to be used for initial beta testing, yet too rough version
 
 <h1>How to install:</h1>
 
 <ol>
 <li>Download the <a href="https://github.com/SuperX-dev/compressor-for-discord.git">Code</a></li>
 <li>Extract it and copy the "Discord Compressor" folder to <code>C:\Program Files\</code></li>
 <li>Run the <code>register.reg</code></li>
   <li>Install <a href="https://www.python.org/downloads/">Python 3</a> and mark the <code>Add Python to Path</code> on the first page of python setup, and allow to disable path lenght limit after installation </li>
<li>Install <a href="https://github.com/GyanD/codexffmpeg/releases/download/2021-09-30-git-3ee4502753/ffmpeg-2021-09-30-git-3ee4502753-full_build.zip">ffmpeg</a> and follow this guide: https://www.thewindowsclub.com/how-to-install-ffmpeg-on-windows-10</li>
  <li>Go to the command prompt or hit the Win+R keys and type <code>cmd</code> and press Ok</li>
 <li>Copy and paste the following commands:<br>
  <code>pip install moviepy<br>
   pip install numpy<br>
   pip install ffmpeg-python<br>
   pip install ffmpeg<br>
   pip install pillow</code>
     <li>Done!</li>
     </ol>
     
<h1>How to use:</h1>
     
   Simply right click on the media file you want (maybe it will not happear in all of them because it doesn´t have support yet, open an issue if that´s the case)
   
   ![image](https://user-images.githubusercontent.com/74361788/135717584-e9b3490f-fe26-4ffb-9ca5-e044c0cc0b3b.png)
     
   And then click in <b>Compress for Discord</b>
   
<h1>Use the Discord Nitro Preset (100MB):</h1>
  Go to the install location: <code>C:\Program Files\Compressor for Discord</code><br>
  Open the <code>config.txt</code> file<br>
  Edit <code>nitro_preset = false</code> to <code>nitro_preset = true</code>
 
