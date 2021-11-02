<div id="top"></div>



<!-- PROJECT LOGO -->
<br />
<div align="center">
  

  <h3 align="center">Plate - A Hobby Project</h3>

  <p align="center">
    A data analyzer and visualizer application for sale data
    <br />
    <a href="https://github.com/ragesh-kr/plate"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
   
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


There are many great POS softwares available in the market, however I did not see any small restaurant owners using the latest state of the art, cloud based solutions which aids them with analytics. Almost 80% of small to mid sized outlets relied on basic standalone applications. 

On a rough average a small outlet/restaurant/supermarket proprietor needs to visit all the outlets on a daily basis for bill closing and sales analysis. I wanted to build an application that would solve this issue without using any high end POS software. Hence PLATE , plate can read excel/csv/db and analyze the data.

Based on the discussions I had with various owners the key metric that they need are

1. Day On Day and Month on Month Sales comparison
2. Comparing sales on every friday, saturday and sunday across weeks and months

Apart from their regular metrics I have added few more like,

Overall sales Trend
1. Best performing and worst performing items based on sale
2. Comparing items based on their sale value
3. Cross sale, which items goes well with which item in a given category
4. Overall performance oof the outlet

Caveats:
* Its is configured to read a particular format for now, format generalization module is yet to be built
* As the project is in initial stage, there is no Mobile support
* I am concentreating on the back end, UI we are using opensource templates

Of course, all the above mentioned points will be covered soon


<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [Plotly.js](https://plotly.com/javascript/)
* [Django](https://www.djangoproject.com/)
* [Python](https://www.python.org/)
* [Pandas](https://pandas.pydata.org/)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

As there is no standardized format built , kindly use the test / demo data set given along with the project

### Prerequisites

Editor of your choice, I have used VSCode
Python 3.7+
Open Network without any corporate firewall restrictions

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._


1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. Install packages from requirement.txt
   ```sh
    $pip install -r requirements.txt
   ```
3. Navigate to your project location and run the below command
   ```sh
    python manage.py runserver
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Modules

## Day On Day and Month on Month Sales Figures

![Alt text](https://github.com/ragesh-kr/plate/blob/ragesh-dev/images/DODSales.PNG?raw=true "Optional Title")



## Type of Meal , and its sales performace

![Alt text](https://github.com/ragesh-kr/plate/blob/ragesh-dev/images/Meals_split_up.PNG?raw=true "Optional Title")

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.





<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [] Add Additional Templates w/ Examples
- [] Add "components" document to easily copy & paste sections of the readme
- [] Multi-language Support
    - [] Chinese
    - [] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are not open yet. Once the project is in a stable state, I shall make it open. Apologies !

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Ragesh Kanagaraj - rageshcv@gmail.com



<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
