package py4jmediator;

import entities.Building;
import entities.Resource;

import java.util.List;
import java.util.Map;

public class MapPresenter {
    private OnMapPresenterCalled onMapPresenterCalled;

    public interface OnMapPresenterCalled{
        void onGoToMenu();
        void onViewInitialized();
        Response onPlaceBuilding(String buildingName, String buildingId);
        boolean onCheckIfCanAffordOnBuilding(String buildingName);
        Response onDeleteBuilding(String buildingId);
        Response onStopProduction(String buildingId);
    }

    public void setOnMapPresenterCalled(OnMapPresenterCalled onMapPresenterCalled){
        this.onMapPresenterCalled = onMapPresenterCalled;
    }

    public void goToMenu(){
    	System.out.println("Going to menu");
        if(onMapPresenterCalled != null){
        	System.out.println("map presenter not null");
            onMapPresenterCalled.onGoToMenu();
        }
    }

    public Response placeBuilding(String buildingName, String buildingId){
        if(onMapPresenterCalled != null)
            return onMapPresenterCalled.onPlaceBuilding(buildingName, buildingId);
        return null;
    }

    public boolean checkIfCanAffordOnBuilding(String buildingName){
    	System.out.println("Checking if can afford");
        if(onMapPresenterCalled != null){
        	System.out.println("mapPresenter not null");
            boolean canAfford =  onMapPresenterCalled.onCheckIfCanAffordOnBuilding(buildingName);
        	System.out.println("Can afford: " + canAfford);
            return canAfford;
        }
        return false;
    }

    public Response deleteBuilding(String buildingId){
        if(onMapPresenterCalled != null)
            return onMapPresenterCalled.onDeleteBuilding(buildingId);
        return null;
    }

    public Response stopProduction(String buildingId){
        if(onMapPresenterCalled != null)
            return onMapPresenterCalled.onStopProduction(buildingId);
        return null;
    }

    public void viewInitialized(){
        if(onMapPresenterCalled != null)
            onMapPresenterCalled.onViewInitialized();
    }

    public void displayMap(){
        Presenter.getInstance().getViewModel().getMapViewModel().displayMap();
    }

    public void init(List<Resource> resources, List<Building> buildings, String texture_one, String texture_two,
                     Map<String, Integer> initialResourcesValues, Map<String, Integer> initialResourcesIncomes){
        Presenter.getInstance().getViewModel().getMapViewModel().init(resources, buildings, texture_one, texture_two,
                initialResourcesValues, initialResourcesIncomes);
    }

    public void updateResourcesValues(Map<String, Integer> actualResourcesValues,
                                      Map<String, Integer> actualResourcesIncomes){
        Presenter.getInstance().getViewModel().getMapViewModel().updateResourcesValues(actualResourcesValues,
                actualResourcesIncomes);
    }

    public void resumeGame(){
        Presenter.getInstance().getViewModel().getMapViewModel().resumeGame();
    }
}
