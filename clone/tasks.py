import celery
import os
import subprocess

from celery import bootsteps


app = celery.Celery('regen_task')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])


@app.task(rate_limit="1/m")
def setup_cpython_repo(event, gh):
    print("Setting up CPython repository")
    if "cpython" not in os.listdir('.'):
        subprocess.check_output(
            f"git clone https://{os.environ.get('GH_AUTH')}:x-oauth-basic@github.com/Mariatta/cpython.git".split())
        subprocess.check_output("git config --global user.email 'mariatta.wijaya@gmail.com'".split())
        subprocess.check_output(["git", "config", "--global", "user.name", "'Mariatta.wijaya'"])
        os.chdir('./cpython')
        print(f"current dir {os.getcwd()}")
        print("Finished setting up CPython Repo")
    else:
        print("cpython directory already exists")


@app.task(rate_limit="1/m")
async def close_pr(event, gh):
    data = {'state': 'closed',
            'maintainer_can_modify': True}
    await gh.patch(event.data["pull_request"]["url"], data=data)
    pr_comment = {
        'body': "close it."
    }

    print("getitem")
    print(pr_comment)

    async for item in gh.getiter('/repos/mariatta/cpython/git/refs/heads'):
        print(item)

    await gh.post(event.data["pull_request"]["comments_url"], data=pr_comment)
# def regen_task():
#     """Backport a commit into a branch."""
#     print(f"current dir {os.getcwd()}")
#     os.chdir('./cpython')
#     print(f"current dir {os.getcwd()}")
#     for l in os.listdir('.'):
#         print(l)
#     print("===")
#     subprocess.check_output(["make", "regen-all"])
#     print("Done make regen-all")
#


class InitRepoStep(bootsteps.StartStopStep):

    async def start(self, c):
        print("Initialize the repository.")
        await setup_cpython_repo()


app.steps['worker'].add(InitRepoStep)