package py4jmediator.MapResponses;

import java.util.Map;

public class EndGameResponse {
    public Map<String, Integer> getDomesticBuildingsSummary() {
        return domesticBuildingsSummary;
    }

    public Map<String, Integer> getIndustrialBuildingsSummary() {
        return industrialBuildingsSummary;
    }

    public Map<String, Integer> getResourcesSummary() {
        return resourcesSummary;
    }

    Map<String, Integer> resourcesSummary;
    Map<String, Integer> domesticBuildingsSummary;
    Map<String, Integer> industrialBuildingsSummary;

    public Map<String, Integer> getDwellersSummary() {
        return dwellersSummary;
    }

    Map<String, Integer> dwellersSummary;

    public int getScore() {
        return score;
    }

    int score;

    public EndGameResponse(Map<String, Integer> resourcesSummary,
                           Map<String, Integer> domesticBuildingsSummary,
                           Map<String, Integer> industrialBuildingsSummary,
                           Map<String, Integer> dwellersSummary,
                           int score){
        this.resourcesSummary = resourcesSummary;
        this.domesticBuildingsSummary = domesticBuildingsSummary;
        this.industrialBuildingsSummary = industrialBuildingsSummary;
        this.dwellersSummary = dwellersSummary;
        this.score = score;
    }

}
