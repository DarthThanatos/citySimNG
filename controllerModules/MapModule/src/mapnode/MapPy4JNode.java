package mapnode;

import controlnode.DispatchCenter;
import controlnode.Py4JNode;
import model.DependenciesRepresenter;
import py4jmediator.MapPresenter;
import py4jmediator.Presenter;
import py4jmediator.Response;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class MapPy4JNode extends Py4JNode implements MapPresenter.OnMapPresenterCalled {
    Thread resourcesThread;
    public boolean updateResources = true;
    public Buildings buildings;
    public Dwellers dwellers;
    Resources resources = null;
    boolean startNewGame = true;


    public MapPy4JNode(DependenciesRepresenter dependenciesRepresenter, DispatchCenter dispatchCenter, String nodeName){
        super(dependenciesRepresenter, dispatchCenter, nodeName);
        resources = new Resources(dr);
        dwellers = new Dwellers(dr);
    }

    @Override
    public void atStart(){
        MapPresenter mapPresenter = Presenter.getInstance().getMapPresenter();
        mapPresenter.setOnMapPresenterCalled(this);
        mapPresenter.displayMap();
        updateResources = true;

        if(startNewGame) {
            resources = new Resources(dr);
            buildings = new Buildings(dr);
            dwellers = new Dwellers(dr);
            mapPresenter.init(resources.getResources(), buildings.getAllBuildings(), dr.getTextureAt(0),
                    dr.getTextureAt(1), resources.getActualResourcesValues(), resources.getActualIncomes());
        }

        resourcesThread = new Thread() {
            public void run() {
                while (updateResources) {
                    resources.updateResources();
                    mapPresenter.updateResourcesValues(resources.getActualResourcesValues(),
                            resources.getActualIncomes());
                    try {
                        Thread.sleep(3000);
                    } catch (Exception e) {
                        System.out.println("Map timer exited while loop");
                    }
                }
                System.out.println("Map timer exited while loop");
            }
        };

        resourcesThread.start();
    }

    @Override
    public void onLoop(){

    }

    @Override
    public void atUnload(){

    }

    @Override
    public void atExit(){
        resourcesThread.interrupt();
        updateResources = false;
        Presenter.getInstance().getMapPresenter().setOnMapPresenterCalled(null);
    }

    @Override
    public void onGoToMenu(){
    	System.out.println("Moving to menu from map");
        moveTo("GameMenuNode");
    }


    @Override
    public Response onPlaceBuilding(String buildingName, String buildingId){
        buildings.placeBuilding(buildingName, buildingId, resources, dwellers);
        return new Response(
                resources.getActualResourcesValues(),
                resources.getActualIncomes(),
                dwellers.getCurrDwellersAmount(),
                dwellers.getCurrDwellersMaxAmount());
    }

    @Override
    public boolean onCheckIfCanAffordOnBuilding(String buildingName){
        return buildings.canAffordOnBuilding(buildingName, resources);
    }

    @Override
    public Response onDeleteBuilding(String buildingId){
        buildings.deleteBuilding(buildingId, resources, dwellers);
        return new Response(
                resources.getActualResourcesValues(),
                resources.getActualIncomes(),
                dwellers.getCurrDwellersAmount(),
                dwellers.getCurrDwellersMaxAmount());
    }

    @Override
    public Response onStopProduction(String buildingId){
        buildings.stopProduction(buildingId, resources, dwellers);
        return new Response(
                resources.getActualResourcesValues(),
                resources.getActualIncomes(),
                dwellers.getCurrDwellersAmount(),
                dwellers.getCurrDwellersMaxAmount(),
                buildings.findBuildingWithId(buildingId).isRunning());
    }
}
