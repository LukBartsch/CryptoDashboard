
# Crypto Dashboard
Web application for data visualization.


## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Project Status](#project-status)
* [Contributing](#contributing)
* [Sources](#sources)
* [Contact](#contact)
* [License](#license)


## General Information
An analytical web application is used to monitor and visualize financial data on the cryptocurrency market. It uses the Dash framework integrated with the Plotly library - all for displaying interactive charts.

Data is collected in real time from several financial services with free API, such as:

* https://coincap.io/
* https://alternative.me/crypto/
* https://polygon.io/
* https://exchangerate.host


## Technologies Used
* [Dash/Plotly](https://dash.plotly.com/)
* [Pandas](https://pandas.pydata.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/) (SQLite as cache memory)


## Features

The main view with a graph of historical cryptocurrency prices dynamically changes depending on the data entered by the user (base currency, selected cryptocurrencies, start date, end date).

![image](https://user-images.githubusercontent.com/98742733/217930069-8d56adfd-58b8-4da6-9352-4ca8bc934632.png)

The chart shows all selected cryptocurrencies and compares them with the base currency. Below the graph there is a dynamic ranking that shows the ten most popular cryptocurrencies and their current parameters. The application uses the SQLite database as a cache, which stores the most current currency prices in case
there is a problem with access to current prices from [API](https://exchangerate.host).

![image](https://user-images.githubusercontent.com/98742733/232784354-09cf7e54-7765-4bea-b344-0b0086ee0a78.png)


Other major financial indicators of the cryptocurrency market presented in the application:

* Fear and Greed Index

![image](https://user-images.githubusercontent.com/98742733/232784901-92ea0267-b407-4cef-b08a-aa19bb189ee9.png)


* Bitcoin Relative Strength Index

![image](https://user-images.githubusercontent.com/98742733/217930362-a20d54d4-edbe-46f2-9a0c-385e554f96b4.png)

* Moving Averages

![image](https://user-images.githubusercontent.com/98742733/218311013-9f99b0c1-f5f0-4579-a898-1c19bc6d43b7.png)

The visitor has the option of choosing the displayed data not only because of the indicator but also for the period of time that interests him. 

## Setup
- Clone repository
* Rename .env.example to `.env` and set your value (get free API key from polygon.io platfrom)
```
api_key_polygon = <your_api_key>
api_key_coincap = <your_api_key>
```

* Install packages from `requirements.txt`
```
pip install -r requirements.txt
```
* Run command
```
python crypto_dashboard.py
```
## Project Status
Due to major restrictions on access to free data (since 03/2025) the application is currently available only as a project on Github.


## Contributing
If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". I will be very grateful for any interesting ideas.


## Sources
This app is inspired by currency dash app by [@szymcio32](https://github.com/szymcio32/currency-monitor-dash-app.git)

## Contact
Created by [@LukBartsch](https://github.com/LukBartsch) - feel free to contact me!

[![LinkedIn][github-shield]][github-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


## License
This project is open source and available under the MIT License.


[github-shield]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[github-url]: https://github.com/LukBartsch
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/lukasz-bartsch/


