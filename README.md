# Pytest reader

## Usage

### General report

```bash
pytest_reader -i full_report.xml
```

```txt
Total duration: 12777.065s
33650 tests ; 1 errors ; 1 failures ; 1037 skipped
 - deepinv.tests.test_models                                    :    3412.01s (26.70%)
 - deepinv.tests.test_optim                                     :    3080.38s (24.11%)
 - deepinv.tests.test_sampling                                  :    2402.32s (18.80%)
 - deepinv.tests.test_datasets                                  :    1208.78s ( 9.46%)
 - deepinv.tests.test_physics                                   :     845.79s ( 6.62%)
 - deepinv.tests.test_generators                                :     459.39s ( 3.60%)
 - deepinv.tests.test_loss                                      :     349.53s ( 2.74%)
 - deepinv.tests.test_utils                                     :     295.90s ( 2.32%)
 - deepinv.tests.test_physics_functional                        :     222.48s ( 1.74%)
 - deepinv.tests.test_distributed                               :     174.72s ( 1.37%)
 - deepinv.tests.test_trainer                                   :     128.09s ( 1.00%)
 - deepinv.tests.test_unfolded                                  :      66.22s ( 0.52%)
 - deepinv.tests.test_external_libraries.TestTomographyWithAstra:      33.87s ( 0.27%)
 - deepinv.tests.test_adversarial                               :      32.43s ( 0.25%)
 - deepinv.tests.test_loss_train                                :      26.34s ( 0.21%)
 - deepinv.tests.test_metric                                    :      20.99s ( 0.16%)
 - deepinv.tests.test_transform                                 :      15.79s ( 0.12%)
 - deepinv.tests.test_deprecated                                :       1.62s ( 0.01%)
 - deepinv.tests.test_noise_model                               :       0.41s ( 0.00%)
 - pytest                                                       :       0.00s ( 0.00%)
Run `pytest_report -c <class_name>` to get a report of a specific class
```


### Class report

A class is either a test module or a test class

```bash
pytest_reader -c deepinv.tests.test_models
```

```txt
deepinv.tests.test_models: 39 tests found
 - test_denoiser_perf                                           :    1255.73s (36.80%)
 - test_denoiser_sigma_color                                    :     965.83s (28.31%)
 - test_denoiser_sigma_gray                                     :     491.87s (14.42%)
 - test_restoration_models                                      :     224.66s ( 6.58%)
 - test_wavelet_denoiser_ths                                    :      91.57s ( 2.68%)
 - test_initialize_3d_from_2d                                   :      63.95s ( 1.87%)
 - test_ncsnpp_net                                              :      59.23s ( 1.74%)
 - test_diffunetmodel                                           :      43.95s ( 1.29%)
 - test_denoiser_color                                          :      43.13s ( 1.26%)
 - test_denoiser_gray                                           :      31.38s ( 0.92%)
 - test_denoiser_1_channel                                      :      27.38s ( 0.80%)
 - test_denoiser_perf_noise_map                                 :      23.20s ( 0.68%)
 - test_wavelet_decomposition                                   :      11.96s ( 0.35%)
 - test_ram_scale                                               :      10.84s ( 0.32%)
 - test_dip_like                                                :      10.39s ( 0.30%)
 - OTHER (24 tests <10.0s)                                      :      56.95s ( 1.67%) Avg. duration: 2.37s
Run `pytest_report -f <function_name>` to get a report of a specific function
```


### Function report

A function is a pytest function and can be parametrized

```bash
pytest_reader -f deepinv.tests.test_models::test_denoiser_sigma_color
```

```txt
test_denoiser_sigma_color: 144 tests ; Total duration: 965.826s
 - test_denoiser_sigma_color[device1-3-deal]                    :     283.05s (29.31%)
 - test_denoiser_sigma_color[device1-2-deal]                    :     200.63s (20.77%)
 - test_denoiser_sigma_color[device0-3-deal]                    :     107.55s (11.14%)
 - test_denoiser_sigma_color[device1-1-deal]                    :      83.92s ( 8.69%)
 - test_denoiser_sigma_color[device0-2-deal]                    :      73.73s ( 7.63%)
 - test_denoiser_sigma_color[device0-1-deal]                    :      27.30s ( 2.83%)
 - test_denoiser_sigma_color[device1-3-bm3d]                    :      17.23s ( 1.78%)
 - test_denoiser_sigma_color[device0-3-bm3d]                    :      14.70s ( 1.52%)
 - test_denoiser_sigma_color[device1-2-bm3d]                    :      13.49s ( 1.40%)
 - test_denoiser_sigma_color[device0-3-epll]                    :      11.18s ( 1.16%)
 - test_denoiser_sigma_color[device0-3-adinv.modelsunet]        :      10.04s ( 1.04%)
 - OTHER (133 cases <10.0s)                                       :     123.01s (12.74%) Avg. duration: 0.92s
```

