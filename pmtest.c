#include <string.h>
#include <stdio.h>

int hacluster_refresh_pacemaker_nodes(const char *node_name)
{
        static char crm_mon_command[] = "crm_mon -X --inactive";
        char buffer[4096];
        int found_nodes = 0;
        FILE *pf;

        char online[10], standby[10], standby_on_fail[10], maintenance[10], pending[10];
        char unclean[10], shutdown[10], expected_up[10], dc[10], the_type[10];

        buffer[sizeof(buffer)-1] = '\0';

        if ((pf = popen(crm_mon_command, "r")) == NULL)
                return -1;

        while(fgets(buffer, sizeof(buffer)-1, pf) != NULL) {
                //printf("%s\n",buffer);

                /* First we need to check whether we are in <nodes> section*/
                if (strstr(buffer, "<nodes>")) {
                        printf("found nodes\n");
                        found_nodes = 1;
                        continue;
                }

                /* Check to see if we overun section */
                if (strstr(buffer, "</nodes>")) {
                        found_nodes = 0;
                        continue;
                }

                /* Collect our node names */
                if (found_nodes && strstr(buffer, node_name)) {
                        printf("buffer:%s",buffer);
                        sscanf(buffer, "%*s %*s %*s online=\"%[^\"]\" standby=\"%[^\"]\" standby_onfail=\"%[^\"]\" maintenance=\"%[^\"]\" pending=\"%[^\"]\" unclean=\"%[^\"]\" shutdown=\"%[^\"]\" expected_up=\"%[^\"]\" is_dc =\"%[^\"]\" %*s type=\"%[^\"]\"",
                                online,
                                standby,
                                standby_on_fail,
                                maintenance,
                                pending,
                                unclean,
                                shutdown,
                                expected_up,
                                dc,
                                the_type
                        );

                printf("result online = %s, standby=%s,standby_onfail=%s,maintenance=%s,pending=%s,unclean=%s,shutdown=%s,expected_up=%s,dc=%s,type=%s\n",
        online,standby,standby_on_fail,maintenance,pending,unclean,shutdown,expected_up,dc,the_type);

                }
        }
        pclose(pf);
        return 0;
}

int main()
{
        int foo = hacluster_refresh_pacemaker_nodes("rhedbvm1");
        printf("return value %d\n",foo);
        return foo;
}
