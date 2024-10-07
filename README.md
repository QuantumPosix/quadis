# quadis
discovery service implementation through various api

Gather Host information - for use in conjunction with performance-redhat/badfish
    
    :[Pre-Requisites] - You need a way to identify the hosts {{rack} : {rack-height}} - {quads.yml naming scheme}.{fqdn}
    
    :We currently use a .csv (provided by your DevOPS or our Hardware VARs) to provide the following things:
        $HOSTNAME which also includes the following dependencies needed for later on steps with:
            :HOST_IP{public,bmc,mac-address} which will use in quadis redfish|badfish api and cli
                :Generally what is received resembles rack-rackheight-model-serial,{list of interface_nic[#]},mac_address
                    :get how the .csv comes from pnt in the ticket for the hosts or include a .csv with the minimum required format needed for foreman api install)
                        continue list format here
             Some new tid-bits of information will have to be entered into foreman or equivalent quads/badfish/redfish endpoint(s)
              Which we currently get from eng-ops (these things like model can now hopefully have a place to be
              scripted to include other modifiers during its creation then pulled into quads via foreman.api or
              have a way for quads to do not worry about host management and then create the necessary steps for a
              successful quads only install (so it generates the flask site, the whole nine yards but commands tied to foreman
            :HOST_SERIAL { redfish.api.vendor.{serial_number_endpoint} }
            
    :[Pre-Requisites] - Quads instructions link to www.theforeman.org setup - foreman domain,subnet hammer-cli{with-config}
    :uses yaml generated subnets list (foreman_api_subnets)
        :{--provisioner} , usage quads --intitial-setup --provisioner { [options]} .. arg2 arg3...
            :: options -
                :standalone (self contained quads-only environment)
                :foreman (uses foreman api and a modified quads.yml to finish setup for the environment)
        :{provisoner_options.$option_initial.py()
        :commands used to set a host (or use quads / foreman fqdn name as host) for a list of commands to be run: --gather , --set , --setup, --display , --verify  : is there a way to ping an ip and see if it is a bmc specifically?
            :maybe see if you can do an api call against (setup resource types for [server, network]) to get system resources from ( /redfish/v1/ , http://10.0.0.10/restconf/data/devices/device/system/ (juniper example))
                :connects to host (type, vendor) and stores information as an ip /serial combo unless hostnames are known
                    :[--setup] (--type) {server}||{network} [OPTIONS] (--host {host} || --host-list {path_to_list) :: need this to check to see if the --display --info is created for the host
                        :Use this to generate the commands needed to integrate into environment use with
                            : --format option with args {xml,json,csv} used to provide info in its required form
                            :maybe we can segment out the different integration pieces here for foreman api, quads api - as well as cli)
                        :[OPTIONS]
                        :[--gather] cli argpase (ex. - quadis --gather (--host || --host-list)  ( --info ( all (default), serial#,memory,network,disk,processor,slot --format xml,json,html) ))
                            : badfish does this already look for examples on:
                                Serial,
                                Memory,
                                Disk,
                                Processor,
                                Network [--type] (--NIC) || (--DPU)  (--vendor) (--name) (--model) (--slot-pcie) (--nic-port) (--nic-mac) (--switch-port)
                                (##new features##)
                                    PCIe Slot,
                                    GPU/DPU(new)  [--info] (--model) (--memory) (--slot-pcie)
                            :may have to include (server || network) --vendor or other intelligent way of different vendor (supermicro,hp,mellanox etc.. api endpoint discovery/execution)
                        :[--set]  (--host || --host-list)
                            :executes setup commands by using the values in --display (saved and verified) to further find and create resources                  :[--verify] (--host || --host-list) (additionally able to select to update specific component --info (serial,memory,network,disk,processor,slot))
                            :this checks the most recent --gather and compares it to --display to see if anything has changed
                                :if it changes we need to be able to then --change  (ex --verify --host $host --change) otherwise it just lists the difference (serves as verification to change)
                        :[--display]  (--host || --host-list) cli argpase ex.- quadis --display {host} ( --info {infotype})
                            :shows the information that was gathered, verified and stored for the resource

                                : download the csv via google api, name it something for the script to run against without interation
                                    : uses the csv data to initially setup foreman host - requires hammer cli or api interaction with foreman.py to work on quads host
                                        :awk -F ',' '{print $4, $31}' lab_hosts.csv | tail -n +2| while read host model ; do echo quads --define-host --host $host --default-cloud cloud01 --host-type baremetal --model $(hammer model list | awk -F '|' '{print $1, $2}' | tail -n +4 | head -n -1 | grep  -w "6" | awk '{print toupper($2)}'); done >> add_quads_hosts
                                            :   quads --define-host --host r1-h01-000-r740xd --default-cloud cloud01 --host-type baremetal --model R740XD-CL-G-1
                                                quads --define-host --host r1-h03-000-r740xd --default-cloud cloud01 --host-type baremetal --model R740XD-CL-G-1
                                                quads --define-host --host r1-h05-000-r740xd --default-cloud cloud01 --host-type baremetal --model R740XD-CL-G-1
                                                quads --define-host --host r1-h07-000-r740xd --default-cloud cloud01 --host-type baremetal --model R740XD-CL-G-1

                            :host setup checklist
                                :determine and sets {host}.{type} {host}.{vendor} and {host}.{model} for correct redfish endpoints
                                :call appropriate redfish module
                                    :BMC
                                        :user info
                                        :network settings
                                        :bios settings
                                            :import default xml for host
                                                :provide way to list xml for import
                                :QUADS
                                    :define-cloud
                                        :creates cloud
                                        :starts creation of new interface/vlan configurations for switch
                                    :define-host - uses info to perform adding hosts to quads
                                        :quads --define-host --host {host}.{{foreman or quads}.domain}.{domain} --default-cloud {default-cloud} --host-type {type} --model $model
                                        :define-interface - also adds in interfaces by scanning {redfishendpoint.slot{list of pcie slots vendor/model} and matching to NIC models or --vendor
                                                :uses generate-host-interfaces.py to pull per host
                                                quads --host {host} --add-interface --interface-name em{i} --interface-mac {em_mac} --interface-switch-ip {em_switch} --interface-port {em_port} --interface-vendor intel --interface-speed {em_speed}

                                    :Network :set interface /vlan membership information per nic on the switch
                                        :aggregate all changes to a single switch change (work on using the switch api way of updating and keeping track of versions by changedate)

                                :Foreman - we may have to add --provisioner {quads,foreman} also allows other custom provisioning options for those that want to adopt it to their own provisioning backend.
                                    :Intial setup
                                        :cat ~/utility/hosts/lab_host.csv | while read hostname hip hmac mip mmac model \\
                                        do hammer host create --name=$hostname --hostgroup=available --model-id=$model --partition-table-id=### --puppet-environment-id=# --location-id=# --organization-id=# \\
                                        --interface=\"type=interface,mac=$hmac,identifier=eno1,name=$hostname,ip=$hip,managed=true,primary=true,provision=true,virtual=false\" \\
                                        --interface=\"type=bmc,provider=ipmi,mac=$mmac,identifier=mgmt,name=mgmt-$hostname,ip=$mip,subnet_id=1,domain_id=1,managed=true,primary=false,provision=false,virtual=false,username=user,password=password"\

                                    :Setup the following based on entries
                                        :hostname - set via csv column with domain attached
                                        :model(have this either read from or overwrite the list of Supported Models "[
                                            ]"" in quads.yml
                                        :host-ip
                                        :host-mac
                                        :management-ip
                                        :management-mac



                                    :user
                                        :current is to create a cloud user that is used in quads for server allocations, maybe have this change to be kerb based and attach kerb users to cloud user login
                                    :roles/filters - uses cloud setup stuff
                                    :subnets -read from quads.yml or {foreman.api};
                                    :domain - read from quads.yml or {foreman.api};

                            :network setup checklist (should we have supported models for network infra as well as server if it is a required type)
                                :requires vendor,model (we need to be able to include different commands to execute based on switch operating system version or different  --variable name (junos commands vs junosEVO or ex4550 vs qfx5200/qfx5130 )
                                    :juniper_$model_base.py \\ may want this to read for other juniper_$model_setup or other juniper_$model_$variable.py if there are specific settings used it could all be passed to the switch after discovery
                                        Switch: {type}{vendor}{model} to read the current api for changes
                                            :


                                        Host:
                                        :set interface /vlan membership information

                                        :makes changes to switch configuration after discovery
                                            :initial
                                                :sets up the switch based on pulling info from quads.yml
                                                    : uses set commands specific per model ?? needed based on total quads clouds
                                                :changes
                                    :mellanox_$model_base.py
                                :changes made by single commit through api change or cli commands
                                    :$interfaces
                                    :$vlan
