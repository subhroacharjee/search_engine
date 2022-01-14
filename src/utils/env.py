import pathlib, os

def home_path():
    return pathlib.Path().home()

def cwd_path():
    return pathlib.Path().cwd()

def get_env_params():
    
    if os.environ.get('env') not in ['production', 'PRODUCTION', 'prod', 'PROD']:
        from dotenv import dotenv_values
        env_path = os.path.join(cwd_path(), '.env')
        os.environ.setdefault(dotenv_values(env_path))
        
    return os.environ.copy()

def setup_dev_env(path_to_env):
    env = {}
    print("Setup Environment".center(10))
    env['PORT'] = input("Enter the PORT to be used: ").strip()
    env['DEBUG'] = True if input("Do you want to restart the server after saving (t/f)") in ['t','True','true','yes'] else False


