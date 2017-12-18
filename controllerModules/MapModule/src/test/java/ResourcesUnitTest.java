import entities.Building;
import entities.Resource;

import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import mapnode.Resources;
import model.DependenciesRepresenter;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;

import java.util.*;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

@RunWith(JUnitParamsRunner.class)
public class ResourcesUnitTest {

    @Mock
    private static DependenciesRepresenter dependenciesRepresenter;

    private Map<String, Building> buildings = new HashMap<>();

    @BeforeClass
    public static void initializeTestClass(){
        dependenciesRepresenter = mock(DependenciesRepresenter.class);

        List<Resource> resourcesList = new ArrayList<>();

        Resource r1 = new Resource("Wood", "None", "None", "");
        Resource r2 = new Resource("Grain", "None", "None", "");
        Resource r3 = new Resource("Gold", "None", "None", "");
        Resource r4 = new Resource("Bread", "None", "None", "");


        resourcesList.add(r1);
        resourcesList.add(r2);
        resourcesList.add(r3);
        resourcesList.add(r4);

        Map<String, Integer> basicResourcesIncome = new HashMap<>();
        basicResourcesIncome.put("Wood", 3);
        basicResourcesIncome.put("Grain", 0);
        basicResourcesIncome.put("Gold", 0);
        basicResourcesIncome.put("Bread", 0);

        when(dependenciesRepresenter.getModuleData("resourcesList")).thenReturn(resourcesList);
        when(dependenciesRepresenter.getModuleData("incomes")).thenReturn(basicResourcesIncome);
    }

    @Before
    public void initializeTest() {
        Map<String, Integer> fieldProduces = new HashMap<>();
        fieldProduces.put("Grain", 3);
        fieldProduces.put("Wood", 0);
        fieldProduces.put("Gold", 0);
        fieldProduces.put("Bread", 0);
        Map<String, Integer> fieldConsumes = new HashMap<>();
        fieldConsumes.put("Wood", 3);
        fieldConsumes.put("Grain", 0);
        fieldConsumes.put("Gold", 0);
        fieldConsumes.put("Bread", 0);
        Map<String, Integer> fieldResourcesCost = new HashMap<>();
        fieldResourcesCost.put("Wood", 10);
        fieldResourcesCost.put("Grain", 0);
        fieldResourcesCost.put("Gold", 0);
        fieldResourcesCost.put("Bread", 0);

        Building field = new Building("Field", "None", "None", 2, fieldProduces,
                fieldConsumes, fieldResourcesCost, "", "Industrial", "", "Worker");
        buildings.put(field.getName(), field);

        Map<String, Integer> houseProduces = new HashMap<>();
        houseProduces.put("Grain", 0);
        houseProduces.put("Wood", 0);
        houseProduces.put("Gold", 1);
        houseProduces.put("Bread", 0);
        Map<String, Integer> houseConsumes = new HashMap<>();
        houseConsumes.put("Wood", 0);
        houseConsumes.put("Grain", 0);
        houseConsumes.put("Bread", 1);
        houseConsumes.put("Gold", 0);
        Map<String, Integer> houseResourcesCost = new HashMap<>();
        houseResourcesCost.put("Wood", 15);
        houseResourcesCost.put("Grain", 0);
        houseResourcesCost.put("Gold", 0);
        houseResourcesCost.put("Bread", 0);

        Building house = new Building("House", "None", "None", 2, houseProduces,
                houseConsumes, houseResourcesCost, "", "Domestic", "", "Worker");
        buildings.put(house.getName(), house);
    }

    @Test
    @Parameters({"Field, Wood, 5",
                 "House, Wood, 7"})
    public void addResourcesFromBuildingDestructionTest(String buildingName, String resourceName, int woodAmount){
        // given
        Resources resources = new Resources(dependenciesRepresenter);
        Building building = buildings.get(buildingName);

        // when
        resources.addResourcesFromBuildingDestruction(building);

        // then
        assertEquals(woodAmount, resources.getActualResourcesValues().get(resourceName), 0.0);
    }

    @Test
    @Parameters({"Field, 1, true, Grain, -1, Wood, 5",
                 "Field, 1, false, Grain, 0, Wood, 5",
                 "Field, 2, true, Grain, -3, Wood, 6",
                 "House, 1, true, Gold, 0, Bread, 1",
                 "House, 2, true, Gold, -1, Bread, 1",
                 "House, 2, false, Gold, 0, Bread, 1"})
    public void subBuildingsBalanceTest(String buildingName, int workingDwellers, boolean isProducing, String incomeResName,
                                        int income, String consumedResName, int balance){
        // given
        Resources resources = new Resources(dependenciesRepresenter);
        Building building = buildings.get(buildingName);
        building.setWorkingDwellers(workingDwellers);
        building.setProducing(isProducing);

        // when
        resources.subBuildingsBalance(building);

        // then
        assertEquals(income, resources.getActualResourcesIncomes().get(incomeResName), 0.0);
        assertEquals(balance, resources.getResourcesBalance().get(consumedResName), 0.0);
        assertEquals(income, resources.getResourcesBalance().get(incomeResName), 0.0);
    }

    @Test
    @Parameters({"Field, Wood, -10",
                 "House, Wood, -15"})
    public void subBuildingCost(String buildingName, String resName, int expectedWoodAmount){
        // given
        Resources resources = new Resources(dependenciesRepresenter);
        Building building = buildings.get(buildingName);

        // when
        resources.subBuildingsCost(building);

        // then
        assertEquals(expectedWoodAmount, resources.getActualResourcesValues().get(resName), 0.0);
    }

    @Test
    @Parameters({"Field, Wood, 0, 0",
                 "Field, Wood, 1, 2",
                 "Field, Wood, 2, 3",
                 "House, Bread, 1, 1",
                 "House, Bread, 2, 1"})
    public void addBuildingConsumptionTest(String buildingName, String resName, int workingDwellers,
                                           int expectedConsumption){
        // given
        Resources resources = new Resources(dependenciesRepresenter);
        Building building = buildings.get(buildingName);
        building.setWorkingDwellers(workingDwellers);

        // when
        resources.addBuildingConsumption(building);

        // then
        assertEquals(expectedConsumption, resources.getActualResourcesConsumption().get(resName), 0.0);
    }

    @Test
    @Parameters({"Field, Wood, 0, 0",
                 "Field, Wood, 1, -2",
                 "Field, Wood, 2, -3",
                 "House, Bread, 1, -1",
                 "House, Bread, 2, -1"})
    public void subBuildingConsumptionTest(String buildingName, String resName, int workingDwellers,
                                           int expectedConsumption){
        // given
        Resources resources = new Resources(dependenciesRepresenter);
        Building building = buildings.get(buildingName);
        building.setWorkingDwellers(workingDwellers);

        // when
        resources.subBuildingConsumption(building);

        // then
        assertEquals(expectedConsumption, resources.getActualResourcesConsumption().get(resName), 0.0);
    }
}

