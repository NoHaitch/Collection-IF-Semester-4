<!-- Back to Top Link-->
<a name="readme-top"></a>


<br />
<div align="center">
  <h1 align="center">CINEMANAGER</h1>

  <p align="center">
    <h3>Film and Series Tracker</h3>

<!-- [![MIT License][license-shield]][license-url] -->

</div>


<!-- CONTRIBUTOR -->
<div align="center" id="contributor">
  <strong>
    <h3>Made By: K01-G07</h3>
    <table align="center">
      <tr>
        <td>NIM</td>
        <td>Nama</td>
      </tr>
      <tr>
        <td>10023519 </td>
        <td>Muhammad Fiqri</td>
      </tr>
      <tr>
        <td>13522037 </td>
        <td>Farhan Nafis Rayhan</td>
      </tr>
      <tr>
        <td>13522071 </td>
        <td>Bagas Sambega Rosyada</td>
      </tr>
      <tr>
        <td>13522091  </td>
        <td>Raden Francisco Trianto Bratadiningrat</td>
      </tr>
    </table>
  </strong>
  <br>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#instruction">Instruction</a></li>
      </ul>
    </li>
  <li>
  <details>
    <summary><a href="#modules">Modules</a></summary>
    <ol>
      <li><a href="#1-module-xxxx">Module 1</a></li>
      <li><a href="#2-module-xxxx">Module 2</a></li>
      <li><a href="#2-module-xxxx">Module 3</a></li>
    </ol>
  </details>
  </li>
    <li><a href="#database-table">Database Tables</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## External Links

- [Linktr RPL](https://linktr.ee/RPL2024)
- [Drive RPL](https://drive.google.com/drive/folders/1JYVbNc6_MfQwp76l9v5rimrjboutvF1_)
- [Spesifikasi Tugas](https://docs.google.com/document/d/174aWdTz-qlKkOMgx_bwCn9EYWQDNIuF9tjxXqrDLoJs/edit)
- [Teams](https://docs.google.com/spreadsheets/d/1yxCgABz1UaWUg5Sqp8KnaFT1WjLmd-1r_zzBHxeWQwg/edit#gid=1251947374)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ABOUT THE PROJECT -->
## About The Project

Cinemanager is a film and series tracker application that allows
users to track their favorite films and series. Users can add films
and series to their watchlist, rate and review them, and track their
progress. Cinemanager also provides a recommendation feature based 
on the user's watchlist and review history.

This project is made as a final project for IF2210 - Software Engineering course in the 2024 semester.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Project dependencies  

* Python 3.12
  ```sh
  # in Linux
  sudo apt install python3
  ```
* Python libraries in `requirements.txt`
  ```sh
  pip install -r requirements.txt
  ```
    

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

_How to install and use your project_

1. Clone the repo
   ```sh
   git clone https://gitlab.informatika.org/cinemanager/cinemanager.git
   ```
2. Install Python libraries
   ```sh
   pip install -r requirements.txt
   ```
3. Run the program
   ```sh
     python main.py
   ```
NOTE: the current program haven't been refactored for general use, 
Currently the program can only run correctly when using intelij IDE.
Using other IDE may cause the program to not run correctly.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- INSTURCTION -->
## Instruction

To run the program, you can use the following command:

```sh
python main.py
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Modules -->
## Modules

### Task Distribution

|         Module Name         |    Assigned To     |
|:---------------------------:|:------------------:|
|         Tambah Film         |      13522071      |
|        Tambah Series        |      13522071      |
|   Perbarui Progres Tonton   | 13522037, 13522091 |
|      Perbarui Komentar      |      13522091      |
|       Perbarui Status       |      13522091      |
|         Tambah Data         | 13522071, 13522091 |
|       Perbarui Status       |      13522091      |
|       Perbarui Review       |      13522091      |
| Perbarui Daftar Film Series | 13522037, 13522091 |
|  Perbarui Data Film Series  | 13522037, 13522091 |
|  Filter Berdasarkan Genre   |      13522071      |
|  Sortir Berdasarkan Rating  |      13522037      |
|      Tampilkan Progres      | 13522071, 13522091 |
|    Olah Data Film Series    |      13522037      |
|       Tampilkan Data        |      13522091      |
|         Cinemanager         |      13522091      |

### 1. Tambah Film
### 2. Tambah Series
### 3. Perbarui Progres Tonton
### 4. Perbarui Komentar
### 5. Perbarui Status
### 6. Tambah Data
### 7. Perbarui Status
### 8. Perbarui Review
### 9. Perbarui Daftar Film Series
### 10. Perbarui Data Film Series
### 11. Filter Berdasarkan Genre
### 12. Sortir Berdasarkan Rating
### 13. Tampilkan Progres
### 14. Olah Data Film Series
### 15. Tampilkan Data
### 16. Cinemanager

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Database Table -->
## Database Table

Here are all the dabase table implemented using SQLite

### Table Genre

| Attribute     | Data Type | Constraint  |
|---------------|-----------|-------------|
| genre_name    | TEXT      | Primary Key |

### Table Categorize

| Attribute     | Data Type | Constraint                                             |
|---------------|-----------|--------------------------------------------------------|
| id_item       | INTEGER   | Primary Key, Foreign Key references WatchItem(id_item) |
| genre_name    | TEXT      | Primary Key, Foreign Key references Genre(genre_name)  |

### Table WatchItem

| Attribute     | Data Type | Constraint  |
|---------------|-----------|-------------|
| id_item       | INTEGER   | Primary Key |
| title         | TEXT      |             |
| poster        | TEXT      |             |
| synopsis      | TEXT      |             |

### Table Review

| Attribute     | Data Type | Constraint                                             |
|---------------|-----------|--------------------------------------------------------|
| id_item       | INTEGER   | Primary Key, Foreign Key references WatchItem(id_item) |
| rating        | REAL      |                                                        |
| comment       | TEXT      |                                                        |

### Table Film

| Attribute         | Data Type | Constraint                                             |
|-------------------|-----------|--------------------------------------------------------|
| id_item           | INTEGER   | Primary Key, Foreign Key references WatchItem(id_item) |
| duration_film     | INTEGER   |                                                        |
| duration_progress | INTEGER   |                                                        |

### Table Series

| Attribute         | Data Type | Constraint                                             |
|-------------------|-----------|--------------------------------------------------------|
| id_item           | INTEGER   | Primary Key, Foreign Key references WatchItem(id_item) |
| total_episode     | INTEGER   |                                                        |
| current_episode   | INTEGER   |                                                        |

### Table Episode

| Attribute         | Data Type | Constraint                                          |
|-------------------|-----------|-----------------------------------------------------|
| id_item           | INTEGER   | Primary Key, Foreign Key references Series(id_item) |
| episode_number    | INTEGER   | Primary Key                                         |
| title             | TEXT      |                                                     |
| duration_episode  | INTEGER   |                                                     |
| duration_progress | INTEGER   |                                                     |

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
<!-- ## Licensing -->

<!-- The code in this project is licensed under MIT license. -->
<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->

<br>
<h3 align="center"> THANK YOU! </h3>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- [license-shield]: https://img.shields.io/badge/License-MIT-yellow
[license-url]: https://github.com/NoHaitch/Repository_Template/blob/main/LICENSE -->
