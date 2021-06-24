import optuna

from output_results_funcs import output_results


def sample_func(x, y, z):
    # func
    ret = (x - 5) ** 2 + (y - 5) ** 2 + (z - 5) ** 2

    return ret


def objective(trial):

    # variable
    x = trial.suggest_uniform('x', -10, 10)
    y = trial.suggest_uniform('y', -10, 10)
    z = trial.suggest_uniform('z', -10, 10)

    # func
    ret = sample_func(x, y, z)

    return ret


def main():
    n_trials = 100
    # output_type = 'standard'
    output_type = 'maximum'
    # output_mode_list = ['plotly', 'pyplot']
    output_mode_list = ['plotly']

    study = optuna.create_study()
    study.optimize(objective, n_trials=n_trials)

    # study.best_params
    output_results(study, output_type=output_type, output_mode_list=output_mode_list)


if __name__ == '__main__':
    main()
