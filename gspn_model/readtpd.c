#define MAX_TOKEN 32767


#include <stdio.h>
#include <stdlib.h>

char  netname[1000];
char  filename[1000];
char  snodeid[10];

void store_double(double *, FILE *);
/*
  double * valp;
  FILE * fp;
*/

void load_double(double * , FILE *);
/*
  double * valp;
  FILE * fp;
*/

float get_average(char *, int nodeid);


unsigned sub_num, group_num, trans_num, place_num;

int main(int argc, char ** argv)
{
    int nodeid = -1;

    if (argc < 2) {
        printf("ERROR: no net name !\n");
        exit(1);
    }
    sprintf(netname, "%s", argv[1]);
    if(argc == 3){
        sprintf(snodeid, "%s", argv[2]);
        nodeid = atoi(snodeid);
    }


    


    get_average(netname, nodeid);




    
}

float get_average(char  netname[1000], int nodeid){
    FILE  *grgfp, * tpdfp;
    double mp;
    double mint, maxt;
    long jj, n;
    sprintf(filename, "%s.grg", netname);
    if ((grgfp = fopen(filename, "r")) == NULL) {
        printf("can_t_open %s\n", filename);
        exit(1);
    }
    /* read number of objects in the net */

    

    fscanf(grgfp, "%d %d %d %d\n", &sub_num, &place_num, &group_num, &trans_num);
    //printf("the net  %s has %d places\n", netname, place_num);
    //printf("Observe: the places are ordered according to their position in the file .net\n");
    fclose(grgfp);

    sprintf(filename, "%s.tpd", netname);
    if ((tpdfp = fopen(filename, "r")) == NULL) {
        printf("can_t_open %s\n", filename);
        exit(1);
    }

    for (n = 1; n <= place_num; n++) {
            double sumprob = 0;
            double average = 0;
            load_double(&mint, tpdfp);
            load_double(&maxt, tpdfp);
            for (jj = 0; jj <= maxt - mint ; jj++) {
                load_double(&mp, tpdfp);
                sumprob += mp;
                average += mp * jj;
                //printf("P(p%ld): %ld\n", n, jj/*,mp*/);
            }
            if(n == nodeid){
                //printf("La media del nodo %d e': %f",nodeid, average);
                (void) fclose(tpdfp);
                return average;
            }
            //printf("\tE[p%ld]: %f\n", n, average);
    }
    (void) fclose(tpdfp);
    return (float)0;
}

void store_double(double *dval, FILE *fp) {
    char *dv = (char *)dval;
    /* Init store_double */
    register unsigned i = sizeof(double);

    for (; i-- ; dv++)
        putc(*dv, fp);
}/* End store_double */

void load_double(double *dval, FILE *fp) {
    char *dv = (char *)dval;
    /* Init load_double */
    register unsigned i = sizeof(double);

    for (; i-- ; dv++)
        *dv = getc(fp);
}/* End load_double */
