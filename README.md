This collects and updates the amount of issues and pull requests with "open" status in different periods of time.

Right now, it is "hardcoded" to work with the Selenium project, future work should enable the community to visualize
their desired repos.

Have a look!

![image](https://user-images.githubusercontent.com/5992658/116539090-a93a9580-a8e8-11eb-8428-a528315bb013.png)


---

Setup instructions are WIP

Create a virtual environment

`python3 -m venv .venv`

`source .venv/bin/activate`

Install `pipenv`

`pip install pipenv`

`pipenv install`

`export GITHUB_ORG`
`export GITHUB_REPO`
`export GITHUB_TOKEN`

`pipenv run get_stats`
