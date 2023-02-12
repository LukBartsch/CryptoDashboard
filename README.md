
# Crypto Dashboard
Web application for data visualization. You can see [_here_](https://crypto-dashboard-6w9a.onrender.com/).


## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Project Status](#project-status)
* [Sources](#sources)
* [Contact](#contact)
* [License](#license)


## General Information
An analytical web application is used to monitor and visualize financial data on the cryptocurrency market. It uses the Dash framework integrated with the Plotly library - all for displaying interactive charts.

Data is collected in real time from several financial services with free API, such as:

* https://coincap.io/
* https://alternative.me/crypto/
* https://polygon.io/


## Technologies Used
* Dash/Plotly
* Pandas
* Python-Forex


## Features

The main view with a graph of historical cryptocurrency prices dynamically changes depending on the data entered by the user (base currency, selected cryptocurrencies, start date, end date).

![image](https://user-images.githubusercontent.com/98742733/217930069-8d56adfd-58b8-4da6-9352-4ca8bc934632.png)

The chart shows all selected cryptocurrencies and compares them with the base currency. Below the graph there is a dynamic ranking that shows the ten most popular cryptocurrencies and their current parameters.

![image](https://user-images.githubusercontent.com/98742733/218312289-19e871c0-c1c0-4f13-a24b-933e59fa0f13.png)

Other major financial indicators of the cryptocurrency market presented in the application:

* Fear and Greed Index

![image](https://user-images.githubusercontent.com/98742733/218311094-2a34c940-31f2-443c-80a7-dc40b3069744.png)

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
Application deployed in beta version on free cloud hosting that is synchronized with GitHub. However, when starting the application for the first time, wait a few seconds to wake up the server on which the application is installed.
In the future, the application will be developed in terms of:
* Optimization of operation
* Refinement of the graphical interface
* Preventing to data errors

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


