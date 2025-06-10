def check_obs(observation, value):
    # check HR
    if observation == 'HR':
        if 60 <= value < 100:
            return 'NORMAL'
        else:
            return 'ABNORMAL'
    # check O2
    elif observation == 'O2_SATS':
        if value >= 92:
            return 'NORMAL'
        else:
            return 'ABNORMAL'


# Define get_pt_details below
