/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package c3ucb;
import java.util.Hashtable;
import Jama.Matrix;
import java.util.Enumeration;

/**
 *
 * @author wudi
 */
public class C3UCB {
    private int k;
    private int pool_size;
    private boolean usingUser; //decide whether to use user feature or not
    private Parameters params;
    private String[] app_list;
    private Matrix af; //matrix consisting of Apps feature
    private Hashtable xf_hist; // Hashtable to store history of x features, where key is user id and value is corresponding xf
    
    public C3UCB(Setting s){
        this.k = s.sizeOfAction;
        this.pool_size = s.numOfApps;
        this.usingUser = s.userInfo;
        this.params = new Parameters(s);

        this.af = getAppFeature();
        this.app_list = getAppID();
        /*
        this.xf_hist = new Matrix[1];
        this.xf_hist[0] = new Matrix(1,s.d);
                */
        this.xf_hist = new Hashtable();
    }
    
    public String[] recommendApps(String uid){ //The interface must give a user id to C3UCB
        if(usingUser) return recommend_withUser(uid);
        else return recommend_noUser(uid);
    }
    
    public void updateAppPool(){
        af = getAppFeature();
        app_list = getAppID(); 
    }

    private String[] recommend_withUser(String uid) {
        Matrix uf = getUserFeature(uid);
        Matrix xf = computeOuterProduct(af, uf);
        double[] UCBs = calculateUCB(params.theta, xf, params.beta, params.V);
        int[] app_idx = getTopKApps();
        String[] action = new String[k];
        for(int i=0; i<app_idx.length; i++) { action[i] = app_list[app_idx[i]]; }
        addToHistory(xf, app_idx, uid);
        return action;
    }
    
    private String[] recommend_noUser(String uid) {
        Matrix xf = af;
        double[] UCBs = calculateUCB(xf);
        int[] app_idx = getTopKApps();
        String[] action = new String[k];
        for(int i=0; i<app_idx.length; i++) { action[i] = app_list[app_idx[i]]; }
        addToHistory(xf, app_idx, uid);
        return action;
    }
    
    private String[] getAppID(){
        return new String[]{"abc","cvd","qwe"};
    }
    
    private Matrix getAppFeature(){
        double[][] tmp = {{1,1,1},{2,2,2}};
        Matrix af = new Matrix(tmp);
        return af;
    }
    
    private Matrix getUserFeature(String uid){
        Matrix uf = new Matrix(new double[]{1,1,1},1);
        return uf;
    }
    
    private Matrix computeOuterProduct(Matrix af, Matrix uf){
        // af's size: (app_r X app_c), uf's size: (1 X usr_c) 
        // TODO: need normalize after product?
        int app_r = af.getRowDimension();
        int app_c = af.getColumnDimension();
        int usr_c = uf.getColumnDimension();
        
        Matrix xf = new Matrix(app_r, app_c * usr_c);
        for (int i=0; i < app_r; i++) {
            double[][] temp = af.getMatrix(i,i,0,app_c-1).transpose().times(uf).getArray(); // outer product of 2 feature vector
            double[] combf = new double[app_c*usr_c]; // flatten the combined feature to 1d
            for (int j=0; j < usr_c; j++){
                for (int k=0; k < app_c; k++) {
                    combf[k*usr_c+j] = temp[k][j]; 
                }
            }
            xf.setMatrix(i, i, 0, app_c*usr_c-1, new Matrix(combf, 1));
        }
        return xf;
    }
    
    //r eturn an array consisting of indices of xf
    // theta: a column vector, 
    // xf: a matrix containing multiple app's combined feature
    // V: square matrix
    private double[] calculateUCB(Matrix theta, Matrix xf, double beta, Matrix V){ 
        int r_num = xf.getRowDimension();
        int d = xf.getColumnDimension();
        double[] UCBs = new double[r_num]; 
        for (int i=0; i < r_num; i++) { //compute each app's ucb
            Matrix xf_i = xf.getMatrix(i,i,0,d-1);
            double vNorm = Math.sqrt(xf_i.times(V.inverse()).times(xf_i.transpose()).get(0,0));
            double tempUcb = xf_i.times(theta).get(0,0) + beta * vNorm;
            tempUcb = tempUcb > 1 ? 1 : tempUcb;
            UCBs[i] = tempUcb;
        }
        
        return UCBs;
    }
    
    private int[] getTopKApps(){
        int[] idx = {1,2,3};
        return idx;
    }
    
    private void addToHistory(Matrix xf, int[] idx, String uid){
        if(!xf_hist.containsKey(uid))
            xf_hist.put(uid, xf.getMatrix(idx,0,xf.getColumnDimension()-1));
    }
    
    public void updateModel(Hashtable feedback){ 
    // supose feedback is a hashtable, the key is the user id, value is a vector(1-d matrix) contains feedback to each recomended app.
    // feedback: cliked = 1, download = 2, ignore = 0(all 0s will be treated as 'dislike')
        Hashtable feedback_d = feedback;
        /*
        Hashtable feedback_d = new Hashtable();
        Enumeration k = feedback.keys();
        while(k.hasMoreElements()){
            String key = (String)k.nextElement();
            feedback_d.put(key,(double)feedback.get(key));
        }*/
        Enumeration k = feedback.keys();
        while(k.hasMoreElements()){
            String uid = (String)k.nextElement();
            Matrix w = (Matrix)feedback_d.get(uid); //get the feedback of one session as w
            w = w.transpose();
            int num_w = w.getRowDimension();
            if(xf_hist.containsKey(uid)){
                Matrix xfs = (Matrix)xf_hist.get(uid); //a set of x feature of one action
                int num_x = xfs.getRowDimension();
                int dim = xfs.getColumnDimension();
                for(int j=0; j<num_x; j++){
                    Matrix xf = xfs.getMatrix(j,j,0,dim-1);
                    params.V = params.V.plus(xf.transpose().times(xf).times(Math.pow(params.gama,2)));
                    xf = xf.times(params.gama);
                    xfs.setMatrix(j,j,0,dim-1,xf);
                }
                Matrix newX = new Matrix(params.X.getRowDimension()+num_x, params.X.getColumnDimension());
                newX.setMatrix(0,params.X.getRowDimension()-1, 0, params.X.getColumnDimension()-1, params.X);
                newX.setMatrix(params.X.getRowDimension(), newX.getRowDimension()-1, 0, params.X.getColumnDimension()-1, xfs);
                params.X = newX;

                w = w.times(params.gama);
                Matrix newY = new Matrix(params.Y.getRowDimension()+num_w,1);
                newY.setMatrix(0, params.Y.getRowDimension()-1, 0, 0, params.Y);
                newY.setMatrix(params.Y.getRowDimension(), newY.getRowDimension()-1, 0, 0, w);
                params.Y = newY;

                Matrix I = Matrix.identity(dim, dim).times(params.lamb);
                params.theta = newX.transpose().times(newX).plus(I).inverse().times(newX.transpose()).times(newY);
                params.beta = params.R * Math.sqrt(Math.log(params.V.det()) - dim * Math.log(params.lamb) - 2 * Math.log(params.delta)) + Math.sqrt(params.lamb);
            }
            else {System.out.println("There is no record of this user");}
        }
    }
    
    public static void main(String[] args) {
        // TODO code application logic here
        Setting set1 = new Setting();
        C3UCB bandit = new C3UCB(set1);
    }

    
    
}
