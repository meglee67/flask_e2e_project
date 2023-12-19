# Web Service
* The idea for this web service is that its a site/form where you are able to select from a drop-down menu, your insurance provider and a medicine, and upon submission, it displays information about the medicine and insurance; if the medicine is covered by the chosen insurance provider and how much the medicine will cost.
* Fufill data requirement option 2: Involve the use of fake data that you create and store in a database and use in your product and then displays data.

# Technologies Used
* I attempted to go for the 110 points so, I attempted to fufill all the web service requirements, using:
    * **Github** - For version control
    * **.env** - environment variables
    * **Flask** - backend
    * **Tailwind** - frontend styling
    * **MySQL GCP Database** 
    * **SQLAlchemy** - ORM
    * **API** - the created API in the api folder within app defines an endpoint that retrieves coverage information for a specified medicine and insurance provider from a database. It cuts out alot of the SQLAlchemy and jsonify, so I decided to put it into its own section to show that I had done it but still wanting to fufill the other webservice requirements (SQLAlchemy, etc.)
    * **Google OAuth** - Used to authenticate and login to my platform
    * **Sentry.io** - used to track errors and log; I would get error emails everytime something went wrong
    * **Docker** - used to containerize the Flask application
    * **Azure Cloud Deployment** - I initally tried to use GCP to deploy, but after many attempts I was unsuccessful. I then switched to Azure and got a successful deployment

# Steps to Run Web Service

## Running without Docker Locally
* to run this without Docker locally, you want to ``git clone`` https://github.com/meglee67/flask_e2e_project.git into your google shell envrionement or your IDE
* cd into the proper directory by doing ``cd flask_e2e_project`` ``cd app``
* then within your terminal, run the command ``python app.py`` and click on the link the appears in the terminal
 
## Running with Docker Locally
* to run this with Docker locally, you want to ``git clone`` https://github.com/meglee67/flask_e2e_project.git into your google shell envrionement or your IDE
* cd into the proper directory by doing ``cd flask_e2e_project`` ``cd app``
* within your terminal run the command ``docker build -t my-app .`` and here you can replace my-app with any image name you want
* then once the image is built, run a container from that image ``docker run -p 8080:80 my-app`` if you renamed my-app to something else in the previous step, it needs to match


## Deploying to Cloud
* Login on the [Azure Portal](https://azure.microsoft.com/en-us/get-started/azure-portal) and search in the bar for App Services
* hit create and hit web app
* after filling out the prompted basic fields you can link to your github and choose a repo 
* after doing that in the deployment center, you can see any attempts at deployment and on the overview page you can find the link.
* here is my link (it is not active as I shut off the service) https://504finalassignmentdeploy.azurewebsites.net/


# .env file structure template
* DB_HOST=ip_address
* DB_DATABASE=database_name
* DB_USERNAME=username_you_set(sometimes it is root)
* DB_PASSWORD=password_you_set
* DB_PORT=3306
* DB_CHARSET=utf8mb4
* FLASK_SECRET_KEY=create_any_password_here
* GOOGLE_CLIENT_ID=find_in_gcp_for_OAuth
* GOOGLE_CLIENT_SECRET=find_in_gcp_for_OAuth

# Screenshots

Here are screenshots from my Azure Cloud deployment; the dashboard and the deployment center
* ![image](https://github.com/meglee67/flask_e2e_project/assets/123908362/70c372cd-03bb-419c-9a13-1987f70a0dae)
* ![image](https://github.com/meglee67/flask_e2e_project/assets/123908362/00e42b17-49dd-4579-a36e-c07978e3954c)

Here is an image of my Sentry.io dashboard
* ![image](https://github.com/meglee67/flask_e2e_project/assets/123908362/68513136-6a81-4149-8207-471624d744f3)

Here are screenshots of my flask app
* ![image](https://github.com/meglee67/flask_e2e_project/assets/123908362/3852a3fe-c3c1-4d75-8108-f47eb84a68d2)
* ![image](https://github.com/meglee67/flask_e2e_project/assets/123908362/510ecad7-2a10-44d4-b4ba-f0b81f13223d)
* ![image](https://github.com/meglee67/flask_e2e_project/assets/123908362/eb75286a-9e7d-4c4c-9de2-ba71c7670d6b)
* ![image](https://github.com/meglee67/flask_e2e_project/assets/123908362/09db6995-7531-446f-9f9e-6f9da8aee964)

Here are screenshots of my SQL database
* ![image](https://github.com/meglee67/flask_e2e_project/assets/123908362/512d73d5-6e5e-41e8-9a9a-77387e33f906)
* ![image](https://github.com/meglee67/flask_e2e_project/assets/123908362/7a8fe0fb-3581-4580-bd6b-49c8f640878d)
* ![image](https://github.com/meglee67/flask_e2e_project/assets/123908362/96f10b62-a758-495d-adaf-d09eed61e683)









