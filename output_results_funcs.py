import os
import datetime
import matplotlib.pyplot as plt
import optuna

from utils import make_dirs, add_suffix, write_image, savefig 


def get_all_params(study):

    trials = [trial for trial in study.trials if trial.state == optuna.trial.TrialState.COMPLETE]
    if len(trials) == 0:
        return None

    all_params = {p_name for t in trials for p_name in t.params.keys()}
    all_params = sorted(list(all_params))

    return all_params


def output_results_plotly(study, all_params, output_dirname, max_resolution_rate, output_type='maximum'):

    print('executing plot_optimization_history...')
    ax = optuna.visualization.plot_optimization_history(study)
    output_filename = 'optimization_history.png'
    write_image(ax, output_dirname, output_filename)

    #comment out
    #if output_type in ['maximum']:
    #    print('executing plot_intermediate_values...')
    #    ax = optuna.visualization.plot_intermediate_values(study)
    #    output_filename = 'intermediate_values.png'
    #    write_image(ax, output_dirname, output_filename)

    if output_type in ['slice', 'standard', 'maximum']:
        print('executing plot_parallel_coordinate...')
        ax = optuna.visualization.plot_parallel_coordinate(study)
        output_filename = 'parallel_coordinate.png'
        write_image(ax, output_dirname, output_filename)

    if output_type in ['maximum']:
        print('executing plot_contour...')
        ax = optuna.visualization.plot_contour(study)
        output_filename = 'contour.png'
        for rate in range(1, max_resolution_rate + 1):
            ax.update_layout(width=int(700 * rate), height=int(500 * rate))
            write_image(ax, output_dirname, output_filename, suffix='_ply_' + str(rate))

    if output_type in ['standard', 'maximum']:
        print('executing plot_contour...')
        output_dirname_tmp = os.path.join(output_dirname, 'contour' + '_ply')
        make_dirs(output_dirname_tmp)
        for param1 in all_params:
            output_dirname_tmp2 = os.path.join(output_dirname_tmp, param1)
            make_dirs(output_dirname_tmp2)
            for param2 in all_params:
                if param1 == param2:
                    continue
                print('executing plot_contour ' + param1 + ', ' + param2 + '...')
                ax = optuna.visualization.plot_contour(study, params=[param1, param2])
                output_filename = param2 + '.png'
                write_image(ax, output_dirname_tmp2, output_filename, suffix='')

    if output_type in ['maximum']:
        print('executing plot_slice...')
        ax = optuna.visualization.plot_slice(study)
        output_filename = 'slice.png'
        write_image(ax, output_dirname, output_filename)

    if output_type in ['slice', 'standard', 'maximum']:
        print('executing plot_slice...')
        output_dirname_tmp = os.path.join(output_dirname, 'slice' + '_ply')
        make_dirs(output_dirname_tmp)
        for param1 in all_params:
            ax = optuna.visualization.plot_slice(study, params=[param1])
            output_filename = param1 + '.png'
            write_image(ax, output_dirname_tmp, output_filename, suffix='')

        print('executing plot_param_importances...')
        ax = optuna.visualization.plot_param_importances(study)
        output_filename = 'param_importances.png'
        write_image(ax, output_dirname, output_filename)

        print('executing plot_edf...')
        ax = optuna.visualization.plot_edf(study)
        output_filename = 'edf.png'
        write_image(ax, output_dirname, output_filename)


def output_results_pyplot(study, all_params, output_dirname, max_resolution_rate, output_type='maximum'):

    print('executing matplotlib.plot_optimization_history...')
    ax = optuna.visualization.matplotlib.plot_optimization_history(study)
    output_filename = 'optimization_history.png'
    savefig(output_dirname, output_filename)

    #comment out
    #if output_type in ['maximum']:
    #    print('executing matplotlib.plot_intermediate_values...')
    #    ax = optuna.visualization.matplotlib.plot_intermediate_values(study)
    #    output_filename = 'intermediate_values.png'
    #    savefig(output_dirname, output_filename)

    if output_type in ['slice', 'standard', 'maximum']:
        # comment out?
        # ValueError: Axis limits cannot be NaN or Inf
        print('executing matplotlib.plot_parallel_coordinate...')
        ax = optuna.visualization.matplotlib.plot_parallel_coordinate(study)
        output_filename = 'parallel_coordinate.png'
        fig = plt.gcf()
        for rate in range(1, max_resolution_rate + 1):
            fig.set_size_inches(6.4 * rate, 4.8 * rate)
            savefig(output_dirname, output_filename, suffix='_plt_' + str(rate), dpi=int(100 * rate))

    if output_type in ['standard', 'maximum']:
        # ax = optuna.visualization.matplotlib.plot_contour(study)
        pass
    
    if output_type in ['slice', 'standard', 'maximum']:
        # ax = optuna.visualization.matplotlib.plot_slice(study)
        # ax = optuna.visualization.matplotlib.plot_param_importances(study)

        print('executing matplotlib.plot_edf...')
        ax = optuna.visualization.matplotlib.plot_edf(study)
        output_filename = 'edf.png'
        savefig(output_dirname, output_filename)


def output_results(study, output_type='maximum', output_mode_list=['plotly', 'pyplot'], max_resolution_rate=3):

    if output_type in ['slice', 'standard', 'maximum']:
        print('best params : {}'.format(study.best_params))
        print('best trial : {}'.format(study.best_trial))
        print('trials_datafarame : {}'.format(study.trials_dataframe()))

    today = datetime.datetime.now()
    today = '{}{:02}{:02}_{:02}{:02}{:02}'.format(str(today.year)[2:], today.month, today.day, today.hour, today.minute, today.second)
    output_dirname = today + 'summary'
    make_dirs(output_dirname)

    print('executing trials_dataframe...')
    output_filename = 'trials.csv'
    output_filepath = os.path.join(output_dirname, output_filename)
    study.trials_dataframe().to_csv(output_filepath)

    # params
    all_params = get_all_params(study)

    if 'plotly' in output_mode_list:
        output_results_plotly(study, all_params, output_dirname, max_resolution_rate, output_type=output_type)

    if 'pyplot' in output_mode_list:
        output_results_pyplot(study, all_params, output_dirname, max_resolution_rate, output_type=output_type)
