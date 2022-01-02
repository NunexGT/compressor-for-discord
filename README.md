# compressor-for-discord
<h2><b>First Beta Version</b></h2>
 A Simple to use all in one media compressor for Discord
 Only to be used for initial beta testing, yet too rough version
 
 <h1>How to install:</h1>
 <h2>Using Windows Binary (Updates may take more time)</h3>
 You can use the <a href="https://github.com/SuperX-dev/compressor-for-discord/releases/download/V0.1.2/compressor4discord-win64.exe">Compressor4Discord installer</a> to just use it right away!
 <h2>Manual method</h2>
 <ol>
 <li>Download the <a href="https://github.com/SuperX-dev/compressor-for-discord/archive/refs/heads/beta_0.1.zip">Code</a></li>
 <li>Extract it and copy the contents of the folder "Discord Compressor" to <code>C:\Compressor4Discord\</code></li>
 <li>Run the <code>register.reg</code></li>
   <li>Install <a href="https://www.python.org/downloads/">Python 3</a> and mark the <code>Add Python to Path</code> on the first page of python setup, and allow to disable path lenght limit after installation </li>
<li>Download <a href="https://github.com/GyanD/codexffmpeg/releases/download/2021-09-30-git-3ee4502753/ffmpeg-2021-09-30-git-3ee4502753-full_build.zip">ffmpeg</a> and follow this guide: https://www.thewindowsclub.com/how-to-install-ffmpeg-on-windows-10</li>
  <li>Go to the command prompt or hit the Win+R keys and type <code>cmd</code> and press Ok</li>
 <li>Copy and paste the following commands, one by one:<br>
  <code>pip install moviepy</code><br>
  <code>pip install numpy</code><br>
  <code>pip install ffmpeg-python</code><br>
  <code>pip install ffmpeg</code><br>
   <code>pip install pillow</code><br>
  <code>pip install winsound</code>
     <li>Done!</li>
     </ol>
     
<h1>How to use:</h1>
     
   Simply right click on the media file you want (maybe it will not happear in all of them because it doesn´t have support yet, open an issue if that´s the case)
   
   ![image](https://user-images.githubusercontent.com/74361788/135717584-e9b3490f-fe26-4ffb-9ca5-e044c0cc0b3b.png)
     
   And then click in <b>Compress for Discord</b>
   
   <b>Note</b>:If video gets higher then 8MB. It will prompt you with some dialogues. Like for you to use Discord Nitro Mode or Divide the videos in parts.
   
<h1>Use the Discord Nitro Preset (100MB) and disable sound notification:</h1>
  Go to the install location: <code>C:\Program Files\Compressor for Discord</code><br>
  Open the <code>config.txt</code> file<br>
  Edit <code>nitro_preset = false</code> to <code>nitro_preset = true</code> if you want to activate Discord Nitro Mode
  <br>Edit <code>sound = true</code> to <code>sound = false</code> to disable notification sound
 
