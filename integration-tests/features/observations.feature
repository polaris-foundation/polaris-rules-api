Feature: Scoring observations sets

    Background: 
        Given I have a valid system JWT
        And there exists an observation set
        And the Trustomer API is running


    Scenario Outline: NEWS2 full observation set scoring
        And temperature value <temperature> is in the observation set
        And systolic blood pressure value <systolic_blood_pressure> is in the observation set
        And diastolic blood pressure value <diastolic_blood_pressure> is in the observation set
        And heart rate value <heart_rate> is in the observation set
        And respiratory rate value <respiratory_rate> is in the observation set
        And spo2 value <spo2> is in the observation set
        And o2 therapy status value <o2_therapy_status> is in the observation set
        And o2 mask value <o2_mask> is in the observation set
        And o2 mask percentage value <o2_mask_percentage> is in the observation set
        And consciousness acvpu value <consciousness_acvpu> is in the observation set
        When I score the observation set according to news2 rules
        Then I see the temperature score is <temperature_score>
        And I see the systolic blood pressure score is <systolic_blood_pressure_score>
        And I see the diastolic blood pressure score is missing
        And I see the heart rate score is <heart_rate_score>
        And I see the respiratory rate score is <respiratory_rate_score>
        And I see the spo2 score is <spo2_score>
        And I see the o2 therapy status score is <o2_therapy_status_score>
        And I see the overall score is <overall_score>
        And I see the score severity is <score_severity>
        And I see the obx abnormal flags is <obx_abnormal_flags>
        And I see the next observation set is due in <next_obs_set_due_in>
        And I see the observation set is full

        Examples:
        | temperature | systolic_blood_pressure | diastolic_blood_pressure | heart_rate | respiratory_rate | spo2 | o2_therapy_status | o2_mask  | o2_mask_percentage | consciousness_acvpu | temperature_score | systolic_blood_pressure_score | diastolic_blood_pressure_score | heart_rate_score | respiratory_rate_score | spo2_score | o2_therapy_status_score | overall_score | score_severity | obx_abnormal_flags | next_obs_set_due_in |
        | 37          | 120                     | 80                       | 60         | 16               | 97   | 0                 | Room Air |                    | Alert               | 0                 | 0                             |                                | 0                | 0                      | 0          | 0                       | 0             | low            | N                  | 12h                 |
        | 37.5        | 109                     | 110                      | 90         | 11               | 95   | 0                 | Room Air |                    | Alert               | 0                 | 1                             |                                | 0                | 1                      | 1          | 0                       | 3             | low       | N               | 4h                  |   
        | 38.1        | 91                      | 110                      | 92         | 21               | 95   | 2                 | Oxygen   | 85                 | Alert               | 1                 | 2                             |                                | 1                | 2                      | 1          | 2                       | 9             | high           | EXTHIGH            | 0m                  |                              

    Scenario Outline: NEWS2 partial observation set scoring
        And temperature value <temperature> is in the observation set
        And systolic blood pressure value <systolic_blood_pressure> is in the observation set
        And diastolic blood pressure value <diastolic_blood_pressure> is in the observation set
        And heart rate value <heart_rate> is in the observation set
        And respiratory rate value <respiratory_rate> is in the observation set
        And spo2 value <spo2> is in the observation set
        And o2 therapy status value <o2_therapy_status> is in the observation set
        And o2 mask value <o2_mask> is in the observation set
        And o2 mask percentage value <o2_mask_percentage> is in the observation set
        And consciousness acvpu value <consciousness_acvpu> is in the observation set
        When I score the observation set according to news2 rules
        Then I see the temperature score is <temperature_score>
        And I see the systolic blood pressure score is <systolic_blood_pressure_score>
        And I see the diastolic blood pressure score is missing
        And I see the heart rate score is <heart_rate_score>
        And I see the respiratory rate score is <respiratory_rate_score>
        And I see the spo2 score is <spo2_score>
        And I see the overall score is <overall_score>
        And I see the score severity is <score_severity>
        And I see the obx abnormal flags is <obx_abnormal_flags>
        And I see the next observation set is due in <next_obs_set_due_in>
        And I see the observation set is partial

        Examples:
        | temperature | systolic_blood_pressure | diastolic_blood_pressure | heart_rate | respiratory_rate | spo2 | o2_therapy_status | o2_mask  | o2_mask_percentage | consciousness_acvpu | temperature_score | systolic_blood_pressure_score | diastolic_blood_pressure_score | heart_rate_score | respiratory_rate_score | spo2_score | overall_score | score_severity | obx_abnormal_flags | next_obs_set_due_in |
        | 37          | 120                     | 80                       | 60         | 16               |      | 0                 | Room Air |                    | Alert               | 0                 | 0                             | 0                              | 0                | 0                      |            | 0             | low            | N                  | 12h                 |
        |             |                         |                          | 160        |                  | 55   | 2                 | Venturi  | 75                 |                    |                    |                               |                                |  3               |                         | 3          | 8             | high           | EXTHIGH            | 0m                  |                              


    Scenario Outline: MEOWS full observation set scoring
        And temperature value <temperature> is in the observation set
        And systolic blood pressure value <systolic_blood_pressure> is in the observation set
        And diastolic blood pressure value <diastolic_blood_pressure> is in the observation set
        And heart rate value <heart_rate> is in the observation set
        And respiratory rate value <respiratory_rate> is in the observation set
        And spo2 value <spo2> is in the observation set
        And consciousness acvpu value <consciousness_acvpu> is in the observation set
        When I score the observation set according to meows rules
        Then I see the temperature score is <temperature_score>
        And I see the systolic blood pressure score is <systolic_blood_pressure_score>
        And I see the diastolic blood pressure score is <diastolic_blood_pressure_score>
        And I see the heart rate score is <heart_rate_score>
        And I see the respiratory rate score is <respiratory_rate_score>
        And I see the spo2 score is <spo2_score>
        And I see the overall score is <overall_score>
        And I see the score severity is <score_severity>
        And I see the obx abnormal flags is <obx_abnormal_flags>
        And I see the next observation set is due in <next_obs_set_due_in>
        And I see the observation set is full

        Examples:
        | temperature | systolic_blood_pressure | diastolic_blood_pressure | heart_rate | respiratory_rate | spo2 | consciousness_acvpu | temperature_score | systolic_blood_pressure_score | diastolic_blood_pressure_score | heart_rate_score | respiratory_rate_score | spo2_score | overall_score | score_severity | obx_abnormal_flags | next_obs_set_due_in |
        | 37          | 120                     | 80                       | 65         | 16               | 97   | Alert               | 0                 | 0                             | 0                              | 0                | 0                      | 0          | 0             | low            | N                  | 12h                 |
        | 37          | 120                     | 80                       | 60         | 16               | 97   | Alert               | 0                 | 0                             | 0                              | 2                | 0                      | 0          | 2             | low-medium     | HIGH               | 6h                  |
        | 37.9        | 90                      | 101                      | 101        | 21               | 92   | Confusion           | 2                 | 2                             | 2                              | 2                | 2                      | 2          | 14            | high           | EXTHIGH            | 30m                 |
    

    Scenario Outline: MEOWS partial observation set scoring
        And temperature value <temperature> is in the observation set
        And systolic blood pressure value <systolic_blood_pressure> is in the observation set
        And diastolic blood pressure value <diastolic_blood_pressure> is in the observation set
        And heart rate value <heart_rate> is in the observation set
        And respiratory rate value <respiratory_rate> is in the observation set
        And spo2 value <spo2> is in the observation set
        And consciousness acvpu value <consciousness_acvpu> is in the observation set
        When I score the observation set according to meows rules
        Then I see the temperature score is <temperature_score>
        And I see the systolic blood pressure score is <systolic_blood_pressure_score>
        And I see the diastolic blood pressure score is <diastolic_blood_pressure_score>
        And I see the heart rate score is <heart_rate_score>
        And I see the respiratory rate score is <respiratory_rate_score>
        And I see the spo2 score is <spo2_score>
        And I see the overall score is <overall_score>
        And I see the score severity is <score_severity>
        And I see the obx abnormal flags is <obx_abnormal_flags>
        And I see the next observation set is due in <next_obs_set_due_in>
        And I see the observation set is partial

        Examples:
        | temperature | systolic_blood_pressure | diastolic_blood_pressure | heart_rate | respiratory_rate | spo2 | consciousness_acvpu | temperature_score | systolic_blood_pressure_score | diastolic_blood_pressure_score | heart_rate_score | respiratory_rate_score | spo2_score | overall_score | score_severity | obx_abnormal_flags | next_obs_set_due_in |
        | 37          |                         | 80                       | 61         | 11               | 97   | Alert               | 0                 |                              | 0                               | 0                | 0                       | 0         | 0             | low            | N                  | 12h                  |
        | 37.9        |                         |                          |            |                  |      | Confusion           | 2                 |                               |                                |                  |                        |            | 4             | medium         | HIGH               | 30m                 |
        |             | 170                     | 112                      |            |                  | 85   | Alert               |                   | 8                             | 8                              |                  |                        | 8          | 24            | high           | EXTHIGH            | 30m                 |
 
