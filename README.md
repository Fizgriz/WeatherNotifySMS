# WeatherNotify v1.0
<h3>Uses Accuweather free API, and Twilio SMS API to go retrieve weather details and send them to user.</h3>

<p>This script was made so that you could get daily weather reports via sms. Features have been added to run the script at will.</p>

<h2>Script Requirements</h2>
<ul>
  <li>Accuweather API</li>
  <ul>
    <li>https://developer.accuweather.com</li>
    <li>Accuweather offers a free API for up to 50 remote calls a day</li>
    <li>You will need to register an App, and use the API key given.</li>
  </ul>
  <li>Twilio SMS API</li>
  <ul>
    <li>https://www.twilio.com/docs/sms/api</li>
    <li>Twilio offers an SMS API for next to nothing in cost.</li>
    <li>You will need to register an app, and use the SID, API key, and a textable number assigned by twilio.</li>
  </ul>
  <li>The .env file</li>
  <ul>
    <li>Before running the .env file needs completed.</li>
    <li>You will need to obtain the API keys and SID from the above requirements first.</li>
    <li>The .env file <b>MUST</b> be in the same directory as the .py file.</li>
  </ul>
</ul>
<h2>Required Libaries</h2>
<ul>
  <li><a href="https://pypi.org/project/requests/2.7.0/">Python Requests Libary</a></li>
  <li><a href="https://www.twilio.com/docs/libraries/python">Python Twilio helper Library</a></li>
  <li><a href="https://pypi.org/project/python-dotenv/">dotenv</a></li>
  <li>argparse</li>
  <li>os.path</li>
</ul>

<h2>Script Uses</h2>
<ul>
  <li>The script can be ran on a scheduled task using the '--skipinput' runtime argument.</li>
  <ul>
    <li>If using the --skipinput arguement, then you need to make sure all the values in the .env file are populated.</li>
    <li>The default run will check for Current tempurature and the daily forecast for the day called.</li>
  </ul>
  <li>The script can be ran on demand, answering runtime inputs or using the --skipinput arguement.</li>
</ul>
