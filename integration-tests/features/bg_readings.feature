Feature: Scoring blood glucose readings

    Background:
        Given the Trustomer API is running

    Scenario Outline: Blood glucose readings are scored with expected output
        Given I have a valid system JWT
        When I score a blood glucose reading of <value> with a tag of <tag>
        Then I see the expected banding is <banding>
        Examples:
            | value | tag                           | banding                   |
            | 3.9   | PRANDIAL-TAG-BEFORE-BREAKFAST | BG-READING-BANDING-LOW    |
            | 4.0   | PRANDIAL-TAG-BEFORE-BREAKFAST | BG-READING-BANDING-NORMAL |
            | 5.2   | PRANDIAL-TAG-BEFORE-BREAKFAST | BG-READING-BANDING-NORMAL |
            | 5.3   | PRANDIAL-TAG-BEFORE-BREAKFAST | BG-READING-BANDING-HIGH   |
            | 3.9   | PRANDIAL-TAG-AFTER-BREAKFAST  | BG-READING-BANDING-LOW    |
            | 4.0   | PRANDIAL-TAG-AFTER-BREAKFAST  | BG-READING-BANDING-NORMAL |
            | 7.7   | PRANDIAL-TAG-AFTER-BREAKFAST  | BG-READING-BANDING-NORMAL |
            | 7.8   | PRANDIAL-TAG-AFTER-BREAKFAST  | BG-READING-BANDING-HIGH   |
            | 3.9   | PRANDIAL-TAG-BEFORE-LUNCH     | BG-READING-BANDING-LOW    |
            | 4.0   | PRANDIAL-TAG-BEFORE-LUNCH     | BG-READING-BANDING-NORMAL |
            | 5.9   | PRANDIAL-TAG-BEFORE-LUNCH     | BG-READING-BANDING-NORMAL |
            | 6.0   | PRANDIAL-TAG-BEFORE-LUNCH     | BG-READING-BANDING-HIGH   |
            | 3.9   | PRANDIAL-TAG-AFTER-LUNCH      | BG-READING-BANDING-LOW    |
            | 4.0   | PRANDIAL-TAG-AFTER-LUNCH      | BG-READING-BANDING-NORMAL |
            | 7.7   | PRANDIAL-TAG-AFTER-LUNCH      | BG-READING-BANDING-NORMAL |
            | 7.8   | PRANDIAL-TAG-AFTER-LUNCH      | BG-READING-BANDING-HIGH   |
            | 3.9   | PRANDIAL-TAG-BEFORE-DINNER    | BG-READING-BANDING-LOW    |
            | 4.0   | PRANDIAL-TAG-BEFORE-DINNER    | BG-READING-BANDING-NORMAL |
            | 5.9   | PRANDIAL-TAG-BEFORE-DINNER    | BG-READING-BANDING-NORMAL |
            | 6.0   | PRANDIAL-TAG-BEFORE-DINNER    | BG-READING-BANDING-HIGH   |
            | 3.9   | PRANDIAL-TAG-AFTER-DINNER     | BG-READING-BANDING-LOW    |
            | 4.0   | PRANDIAL-TAG-AFTER-DINNER     | BG-READING-BANDING-NORMAL |
            | 7.7   | PRANDIAL-TAG-AFTER-DINNER     | BG-READING-BANDING-NORMAL |
            | 7.8   | PRANDIAL-TAG-AFTER-DINNER     | BG-READING-BANDING-HIGH   |
            | 3.9   | PRANDIAL-TAG-OTHER            | BG-READING-BANDING-LOW    |
            | 4.0   | PRANDIAL-TAG-OTHER            | BG-READING-BANDING-NORMAL |
            | 7.7   | PRANDIAL-TAG-OTHER            | BG-READING-BANDING-NORMAL |
            | 7.8   | PRANDIAL-TAG-OTHER            | BG-READING-BANDING-HIGH   |

    Scenario Outline: Blood glucose readings are scored correctly with custom thresholds
        Given I have a valid system JWT
        When I score a blood glucose reading using custom thresholds with <value> and a tag of <tag>
        Then I see the expected banding is <banding>
        Examples:
            | value | tag                           | banding                   |
            | 11    | PRANDIAL-TAG-BEFORE-BREAKFAST | BG-READING-BANDING-HIGH    |
            | 4     | PRANDIAL-TAG-BEFORE-BREAKFAST | BG-READING-BANDING-LOW |
