import os
import json
from pprint import pprint


def get_env_vars():
    lambda_env_vars = {}
    for env_name in os.environ:
        if env_name.startswith('LAMBDA_ENV_'):
            lambda_env_vars[env_name[11:]] = os.getenv(env_name)
    return {"environment_variables": lambda_env_vars}


def get_config_from_template():
    with open('./.chalice/config-template.json') as config_template_fp:
        config = json.load(config_template_fp)
    return config


def get_policy_from_template():
    with open('./.chalice/policy-template.json') as policy_template_fp:
        policy = json.load(policy_template_fp)
    return policy


def save_config(config):
    pprint(config)
    with open('./.chalice/config.json', 'w+') as config_output:
        json.dump(config, config_output, indent=4)


def save_policy(policy):
    pprint(policy)
    with open('./.chalice/policy.json', 'w+') as policy_output:
        json.dump(policy, policy_output, indent=4)


def populate_policy(policy):
    for i, s in enumerate(policy['Statement']):
        if s['Resource'].startswith('POLICY_ENV_'):
            arn = str(os.getenv(s['Resource']))
            policy['Statement'][i]['Resource'] = arn


def main():
    config = get_config_from_template()
    env_vars = get_env_vars()
    for stage in config['stages']:
        for lambda_functions in config['stages'][stage]['lambda_functions']:
            current_config = config['stages'][stage]['lambda_functions'][lambda_functions]
            current_config.update(env_vars)
            config['stages'][stage]['lambda_functions'][lambda_functions] = current_config
    save_config(config)

    policy = get_policy_from_template()
    populate_policy(policy)
    save_policy(policy)


if __name__ == '__main__':
    main()
