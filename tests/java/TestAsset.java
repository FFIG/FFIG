import static org.junit.Assert.assertEquals;
import org.junit.Test;
//import org.ffig.Asset;

public class TestAsset {
    @Test
    public void CDOhasPVofZero()
    {
        Asset cdo = Asset.Asset_CDO_create();
        double pv = cdo.value();
        assertEquals(99.99, pv, 0.0);
    }
}