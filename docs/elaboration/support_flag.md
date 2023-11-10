# Support Flags

## Issue

Issue-01

## Motivation

Currently the support flags calculation is done in the code itself ([createLandscapeConfig()](https://github.tools.sap/hci/landscape/blob/develop/azure/python_lib/landscape_api.py#L36)) and the support must be manifested in the [landscape defintion](https://github.tools.sap/hci/landscape/blob/develop/.pipeline/landscapes/develop.yaml) as well. This is mixing up plain landscape defintion and the skip force flag framework and makes it unclear and cumbersome to maintain. Instead it should be moved out to a dedicated config file, which can be edited easily with a clear distinction of landscape definition and skip force flag framework.

## Architecture

### Relation to Overall CSI Architecture

It will refactor the already existing support flag implementation to source out its defintinion into its own config file.

### Main Architecture Concepts and Decisions

Support flags should be defined and maintained in its own dedicated file, which can be used by the skip force flag framework for the flag calculation later.

Two reasonable approaches can be considered:

1. the support flags will be defined in its very own config file, like the [skip_force_flags.yaml](https://github.tools.sap/hci/landscape/blob/develop/.pipeline/skip_force_flags.yaml).
This file will only contain tests, which are not supported by all landscapes. Instead of assigning the supported tests to landscapes, as it is done right now, the landscapes will be assigned to the tests they support. This will ease reading and calculating the support flags.

    Current approach:

    ```title=".pipeline/landscapes/develop.yaml"
    lane_aws_ci:
        ...
        supports_hana_plugins_apis_tests: true
    lane_azure_ci:
        ...
        supports_hana_pal_service_tests: true
        supports_hana_plugins_apis_tests: true
    ```

    New approach:

    ```title=".pipeline/support_flags.yaml"
    x_tests:
        lane_aws_ci
        lane_azure_ci
        ...

    y_tests:
        lane_azure_ci
        ...
    ```

2. The currently existing `skip_force_flags.yaml` can be extended by support attributes. In this canse the new skip force framework developed in [HANA-18715](https://jira.tools.sap/browse/HANA-18715) can immediately take the support flags into consideration while calculating flags. This might look like the following, although we should consider limiting the scope to not extend the functionality, but only maintain the existing scope (`landscape_is_in`):

    ```title=".pipeline/skip_force_flags.yaml"
    x_tests:
        skip_when:
            - ...
        enforce_when:
            - ...
        supported_when:
            - per_default: true
            ...

    y_tests:
        skip_when:
            - ...
        enforce_when:
            - ...
        supported_when:
            - landscape_type_is_in: ['monitor', ...]
            - landscape_is_in: ['lane_aws_ci', 'lane_azure_ci', ...]
            ...
    ```
