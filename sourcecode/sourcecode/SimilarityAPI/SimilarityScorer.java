import in.ac.iitb.cfilt.similarityapi.*;
import java.util.ArrayList;

class SimilarityScorer{
	public ArrayList<ArrayList<Double>> score(ArrayList<String> hyps, ArrayList<String> refs, ArrayList<ArrayList<Double>> dist){
		SimilarityMeasures smeasures = new SimilarityMeasures();
		boolean useVirtualRoot = true;
		for (int i = 0; i<hyps.size() ; i++ ) {
			for (int j = 0; j<refs.size() ;j++ ) {
				if (dist.get(i).get(j) != 0.0) {
					boolean allMatched = true;
					String[] splittedRefNgrams = refs.get(j).split(" ");
					String[] splittedHypNgrams = hyps.get(i).split(" ");
					if (splittedRefNgrams.length == splittedHypNgrams.length) {
						for (int k=0; k<splittedHypNgrams.length ; k++) {
							String refWord = splittedRefNgrams[k];
							try{
								if (smeasures.getMaxWupSimilarity(splittedRefNgrams[k], splittedHypNgrams[k], useVirtualRoot).similarity < 0.6){
									allMatched = false;
									break;
								}
							} catch (Exception e) {
								if (splittedRefNgrams[k].compareTo(splittedHypNgrams[k]) != 0){
									allMatched = false;
									break;
								}
							}
						}
						if(allMatched){
							dist.get(i).set(j,0.0);
						}
					}
				}
			}
		}
		return dist;
		// return null;
	}
}
