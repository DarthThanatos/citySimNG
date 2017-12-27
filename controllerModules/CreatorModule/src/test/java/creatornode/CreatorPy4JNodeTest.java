package creatornode;

import constants.Consts;
import controlnode.DispatchCenter;
import model.DependenciesRepresenter;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;

import java.util.HashMap;
import java.util.logging.Logger;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import static org.junit.Assert.*;

public class CreatorPy4JNodeTest {
    private static Logger log = Logger.getLogger(CreatorPy4JNode.class.getName());
    @Mock
    private DispatchCenter dispatchCenter;

    private HashMap<String, DependenciesRepresenter> representers;

    @Before
    public void init(){
        representers = new HashMap<>();
        dispatchCenter = mock(DispatchCenter.class);
        when(dispatchCenter.getDispatchData(Consts.LOADER_MODULE, Consts.DEPENDENCIES_REPRESENTERS)).thenReturn(representers);
    }


    private void testMoonMetaData(DependenciesRepresenter moonDependenciesRepresenter){
        assertEquals(moonDependenciesRepresenter.getTextureAt(0), "new\\moon_bg.jpg");
        assertEquals(moonDependenciesRepresenter.getTextureAt(1), "new\\moon_bg2.jpg");
        assertEquals(moonDependenciesRepresenter.getMp3(), "TwoMandolins.mp3");
        assertEquals(moonDependenciesRepresenter.getPanelTexture(), "new\\panel.jpg");
        assertEquals(moonDependenciesRepresenter.getBuildingsNames().size(), 16);
        assertEquals(moonDependenciesRepresenter.getResourcesNames().size(),13);
        assertEquals(moonDependenciesRepresenter.getDwellersNames().size(), 4);
    }

    private void testMoonDeps(){
        DependenciesRepresenter moonDependenciesRepresenter = representers.get("Moon");
        assertNotNull(moonDependenciesRepresenter);
        testMoonMetaData(moonDependenciesRepresenter);
    }

    private void testStrongholdDeps(){
        DependenciesRepresenter strongholdDependenciesRepresenter = representers.get("Stronghold");
        assertNotNull(strongholdDependenciesRepresenter);
    }
    @Test
    public void testDefaultSets(){
        //representers map is filled in the constructor of CreatorNode
        new CreatorPy4JNode(dispatchCenter, "Creator",
                "..\\..\\resources\\sysFiles\\defaultDependencies\\");
         assertEquals(representers.size(), 2);
        testMoonDeps();
        testStrongholdDeps();
    }
}