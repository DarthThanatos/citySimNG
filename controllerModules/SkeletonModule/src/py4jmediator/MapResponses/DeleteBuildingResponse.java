package py4jmediator.MapResponses;

import java.util.List;
import java.util.Map;

public class DeleteBuildingResponse extends BasicResponse {
    public DeleteBuildingResponse(Map<String, Integer> actualResourcesValues, Map<String, Integer> actualResourcesIncomes,
                                 Map<String, Integer> actualResourcesConsumption, Map<String, Integer> resourcesBalance,
                                 int currentDwellersAmount, int currentDwellersMaxAmount){
        super(actualResourcesValues, actualResourcesIncomes, actualResourcesConsumption, resourcesBalance,
                currentDwellersAmount, currentDwellersMaxAmount);
    }
}