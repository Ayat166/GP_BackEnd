# VProva – Virtual Try-On Mobile Application

VProva is an innovative mobile application that allows users to virtually try on clothes using 2D images. By leveraging advanced generative AI models, VProva enhances the online shopping experience, enabling users to visualize how garments would look on them without the need for physical trials.
---

For more details, refer to the [project presentation](https://www.canva.com/design/DAF8m-fqUHM/cQiaBQuOSXSaX_qtPUi73g/edit?utm_content=DAF8m-fqUHM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton).

---

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## About the Project

In the realm of e-commerce, the inability to try on clothes before purchasing poses a significant challenge. VProva addresses this issue by providing a virtual fitting room experience, allowing users to see how clothes would fit and look on them through their mobile devices. This not only enhances user satisfaction but also reduces return rates for online retailers.

## Features

- **Virtual Try-On:** Users can upload their images and virtually try on different outfits.
- **AI-Powered Fitting:** Utilizes the IDM_VTON generative AI model to accurately overlay clothing on user images.
- **User-Friendly Interface:** Intuitive design ensures a seamless user experience.
- **Responsive Design:** Optimized for various mobile devices to ensure accessibility.

## Architecture

The application is structured into two main components:

1. **Frontend (Mobile Application):**
   - Built using Flutter.
   - Handles user interactions, image uploads, and displays the virtual try-on results.

2. **Backend:**
   - Developed with Django REST Framework.
   - Manages API endpoints, user authentication, and communication with the AI model.
   - Processes images and returns the generated try-on results.


## Technologies Used

- **Frontend:**
  - Flutter

- **Backend:**
  - Python
  - Django REST Framework
  - PostgreSQL

- **AI Model:**
  - IDM_VTON

- **Others:**
  - Docker
  - Git & GitHub for version control

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Docker (optional, for containerization)

### Backend Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Ayat166/GP_BackEnd.git
   cd GP_BackEnd
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database:**

   Update the `settings.py` file with your PostgreSQL credentials.

5. **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Run the Server:**

   ```bash
   python manage.py runserver
   ```

### Frontend Setup

[Provide detailed instructions based on the frontend framework used.]

## Usage

1. **Register/Login:**
   - Users can create an account or log in to access the virtual try-on feature.

2. **Upload Image:**
   - Upload a clear 2D image of yourself.

3. **Select Clothing:**
   - Browse and select garments you'd like to try on.

4. **View Results:**
   - The AI model processes the image and displays the virtual try-on result.


## License

[Specify the license under which the project is distributed, e.g., MIT License.]

## Contact

- **Name:** Ayat Ali
- **Email:** [ayatali1661@gmail.com](mailto:ayatali1661@gmail.com)
- **LinkedIn:** [linkedin.com/in/ayat-ali-0795b21b8](https://www.linkedin.com/in/ayat-ali-0795b21b8)
- **GitHub:** [github.com/Ayat166](https://github.com/Ayat166)


