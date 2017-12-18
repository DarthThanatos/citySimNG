import entities.Building;
import mapnode.Buildings;
import model.DependenciesRepresenter;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.Mock;

import java.util.*;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

@RunWith(Parameterized.class)
public class BuildingsUnitTest {

    @Parameterized.Parameter(0)
    public int woodAmount;

    @Parameterized.Parameter(1)
    public boolean canAffordOnField;

    @Parameterized.Parameters
    public static Collection<Object[]> data(){
        Object[][] data = new Object[][] { {7, false}, {10, true}, {15, true} };
        return Arrays.asList(data);
    }

    @Mock
    private DependenciesRepresenter dependenciesRepresenter;

    @Before
    public void initialize(){
        dependenciesRepresenter = mock(DependenciesRepresenter.class);

        List<Building> allBuildings = new ArrayList<>();

        Map<String, Integer> b1Produces = new HashMap<>();
        b1Produces.put("Grain", 2);
        Map<String, Integer> b1Consumes = new HashMap<>();
        b1Consumes.put("Wood", 1);
        Map<String, Integer> b1ResourcesCost = new HashMap<>();
        b1ResourcesCost.put("Wood", 10);

        Building b1 = new Building();
        b1.setName("Field");
        b1.setPredecessor("None");
        b1.setSuccessor("None");
        b1.setDwellersAmount(1);
        b1.setProduces(b1Produces);
        b1.setConsumes(b1Consumes);
        b1.setResourcesCost(b1ResourcesCost);
        b1.setType("Industrial");
        b1.setDwellersName("Worker");

        allBuildings.add(b1);

//        Map<String, Integer> b2Produces = new HashMap<>();
//        b2Produces.put("Gold", 5);
//        Map<String, Integer> b2Consumes = new HashMap<>();
//        b2Consumes.put("Bread", 1);
//        Map<String, Integer> b2ResourcesCost = new HashMap<>();
//        b2ResourcesCost.put("Wood", 20);
//
//        Building b2 = new Building();
//        b2.setName("House");
//        b2.setPredecessor("None");
//        b2.setSuccessor("None");
//        b2.setDwellersAmount(1);
//        b2.setProduces(b2Produces);
//        b2.setConsumes(b2Consumes);
//        b2.setResourcesCost(b2ResourcesCost);
//        b2.setType("Industrial");
//        b2.setDwellersName("Worker");

        when(dependenciesRepresenter.getModuleData("allBuildings")).thenReturn(allBuildings);
    }

    @Test
    public void testCanAffordOnBuilding(){
        // given
        Map<String, Integer> actualResValues = new HashMap<>();
        actualResValues.put("Wood", woodAmount);
        Buildings buildings = new Buildings(dependenciesRepresenter);

        // when
        Boolean canAfford = buildings.canAffordOnBuilding("Field", actualResValues);

        // then
        assertEquals(canAfford, canAffordOnField);
    }

}
