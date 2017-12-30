package corectness.checker;

import constants.Consts;
import controlnode.DispatchCenter;
import creatornode.CreatorPy4JNode;
import model.DependenciesRepresenter;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;

import java.util.HashMap;

import static org.junit.Assert.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class LvlMapperTest {

    private LvlMapper lvlMapper = new LvlMapper();

    @Mock
    private DispatchCenter dispatchCenter;

    @Before
    public void setUp() throws Exception {
        HashMap<String, DependenciesRepresenter> representers = new HashMap<>();
        dispatchCenter = mock(DispatchCenter.class);
        when(dispatchCenter.getDispatchData(Consts.LOADER_MODULE, Consts.DEPENDENCIES_REPRESENTERS)).thenReturn(representers);
        new CreatorPy4JNode(dispatchCenter, "Creator", "..\\..\\resources\\sysFiles\\defaultDependencies\\");

        DependenciesRepresenter lvlDR = representers.get("Moon");
        lvlMapper.mapLevels(
                lvlDR.getGraphsHolder().getResourcesGraphs(),
                lvlDR.getGraphsHolder().getDwellersGraphs(),
                lvlDR.getGraphsHolder().getBuildingsGraphs()
        );
    }

    @Test
    public void testLvlsExist(){
        assertNotNull(lvlMapper.getBuildingsNodesLevels());
        assertNotNull(lvlMapper.getDwellersNodesLevels());
        assertNotNull(lvlMapper.getResourcesNodesLevels());
    }

    @Test
    public void testDwellersLvls(){
        HashMap<String, Integer> dwellersLvls = lvlMapper.getDwellersNodesLevels();
        assertEquals(dwellersLvls.get("Robotnik").intValue(), 0);
        assertEquals(dwellersLvls.get("Inwestor").intValue(), 1);
        assertEquals(dwellersLvls.get("Naukowiec").intValue(), 2);
        assertEquals(dwellersLvls.get("Xenogenetyk").intValue(), 3);
    }

    @Test
    public void testBuildingsLvls(){
        HashMap<String, Integer> buildingsLvls = lvlMapper.getBuildingsNodesLevels();
        assertEquals(buildingsLvls.get("Kopalnia gleju").intValue(), 0);
        assertEquals(buildingsLvls.get("Zrodlo gizmo").intValue(), 0);
        assertEquals(buildingsLvls.get("Fabryka energodropsow").intValue(), 0);

        assertEquals(buildingsLvls.get("Kompleks inwestorow").intValue(), 1);
        assertEquals(buildingsLvls.get("Kopalnia studni przyciagania").intValue(), 1);
        assertEquals(buildingsLvls.get("Fabryka syntetycznych kadlubow").intValue(), 1);

        assertEquals(buildingsLvls.get("Browar").intValue(), 2);
        assertEquals(buildingsLvls.get("Kwatery naukowcow").intValue(), 2);

        assertEquals(buildingsLvls.get("Palac Xenogenetyka").intValue(), 3);
        assertEquals(buildingsLvls.get("Cukiernia").intValue(), 3);

    }


    @Test
    public void testResourcesLvls(){
        HashMap<String, Integer> resourcesLvls = lvlMapper.getResourcesNodesLevels();
        assertEquals(resourcesLvls.get("Glej").intValue(), 0);
        assertEquals(resourcesLvls.get("Owoce").intValue(), 0);
        assertEquals(resourcesLvls.get("Nanoplastik").intValue(), 0);
        assertEquals(resourcesLvls.get("Gizmo").intValue(), 0);

        assertEquals(resourcesLvls.get("Syntetyczne kadluby").intValue(), 1);
        assertEquals(resourcesLvls.get("Witaminy").intValue(), 1);

        assertEquals(resourcesLvls.get("Zdrowy likier").intValue(), 2);
        assertEquals(resourcesLvls.get("Krysztaly efektu masy").intValue(), 2);

        assertEquals(resourcesLvls.get("Alkoholowe desery").intValue(), 3);
    }
}