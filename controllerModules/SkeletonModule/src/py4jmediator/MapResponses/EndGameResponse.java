package py4jmediator.MapResponses;

import java.util.Map;

public class EndGameResponse {
    public Map<String, Integer> getDomesticBuildingsSummary() {
        return domesticBuildingsSummary;
    }

    public Map<String, Integer> getIndustrialBuildingsSummary() {
        return industrialBuildingsSummary;
    }

    Map<String, Integer> domesticBuildingsSummary;
    Map<String, Integer> industrialBuildingsSummary;

    public EndGameResponse(Map<String, Integer> domesticBuildingsSummary,
                           Map<String, Integer> industrialBuildingsSummary){
        this.domesticBuildingsSummary = domesticBuildingsSummary;
        this.industrialBuildingsSummary = industrialBuildingsSummary;
    }

}
