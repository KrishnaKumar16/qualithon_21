Feature: Qualithon contest

  @run
  Scenario: To solve the puzzle and acquire the treasure
    Given I enter the contest
    When I solve the proceed button puzzle
    And I solve the video puzzle
    And I solve the maze puzzle
    And I solve the map puzzle
    And I solve the captcha
    And I solve the socket puzzle
    Then I should be having the treasure