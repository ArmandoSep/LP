$(document).ready(function () {
    // QueryString
    const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
    });
    let email = params.email;
    let ht = params.ht;
    let address = params.address;
    let zip = params.zip;
        // Input
    var form_input = JSON.stringify({
        email: email, help_type: ht, address: address
    });
    
    fetch("https://8itrmxfbjg.execute-api.us-east-1.amazonaws.com/default/LP_VerifyLead-Webflow",{
            method: 'POST',
        headers: {'Accept': 'application/json', 'Content-Type': 'application/json'},
        body: form_input,
    })
    // response
    .then(res => res.json())
    .then(json => {
        const val_response = json;
        const need_name = val_response["need_name"];
        const need_phone = val_response["need_phone"];
        const need_company = val_response["need_company"];
        const hub_id = val_response["hid"];
        const contact_name = val_response["first_name"];
        const existing_deal = val_response["existing_deal"];
        // Show main
        const $main_section = $('#main-section');
        const $error_section = $('#error-section');
        $main_section.toggleClass('mainsection--show', existing_deal === 'N');
        $error_section.toggleClass('errorsection--show', existing_deal === 'Y');
        $('#deal-section').toggleClass('dealsection--show', ['emd', 'dl', 'closer', 'dispo', 'tc'].indexOf(ht) > -1);
        $('#data-section').toggleClass('datasection--show', ['data', 'dialer'].indexOf(ht) > -1);
        $('#experience-div').toggleClass('experience--show', ht == "dialer");
        $('#data-title').toggleClass('datatitle--hide', ht == "dialer");
        $('#zoom-section').toggleClass('zoomsection--show', ht == "zoom");
        $('#dates-div').toggleClass('dates--show', ['emd', 'dispo'].indexOf(ht) > -1);
        $('#funding-section').toggleClass('fundingsection--show', ['emd'].indexOf(ht) > -1);
        
        // Clean contact var
        if (need_name == 'Y'){
            $("#first_name-2").prop('required',true);
        $("#last_name-2").prop('required',true);
        } else{
            $('#name-div').toggleClass('name--hide')
        };
        if (need_phone == 'Y'){
            $("#phone").prop('required',true);
        } else{
            $('#phone-div').toggleClass('phone--hide')
        };
        if (need_company == 'Y'){
            $("#company").prop('required',true);
        } else{
            $('#company-div').toggleClass('company--hide')
        };
        // Populate fields
        if (ht == "emd"){
            var $help = "Want funding to keep scaling? We are here to help!";
        document.querySelector('#submit-button').value = '👉 Apply';
        // required fields
        $("#ftype").prop('required',true);
        $("#famount").prop('required',true);
        $("#fdate").prop('required',true);
        $("#purchase-contract").prop('required',true);
        }
        else if (ht == "dl"){
            var $help = "Want to monetize a deal where the numbers don't work out? We are here to help!";
            document.querySelector('#submit-button').value = '👉 Monetize lead';
            $("#motivation").prop('required',true);
            $("#mls_status-2").prop('required',true);

            // Show why dead lead and last conversation with seller fields
            $('#deadlead_details').addClass('show');
            $("#why_dl").prop('required',true);
            $("#spoke_seller").prop('required',true);

        }
        else if (ht == "closer"){
            var $help = "Need assitance from a Lanza Team closer? We are here to help!";
            document.querySelector('#submit-button').value = '👉 Request closer';
        }
        else if (ht == "dispo"){
            var $help = "Want to stay focused on acquisitions and delegate the dispo? We are here to help!";
            document.querySelector('#submit-button').value = '👉 Request dispo';
            $('#dispo-sec').addClass('dispo--show');
            $('#add_comments1').attr('placeholder','Specific instruction for COE, age of majors (HVAC, roof, foundation), it’s near a train track, etc');
        }
        else if (ht == "tc"){
            var $help = "Want to stay focused on new deals and delegate the Transaction Coordinating work? We are here to help!";
            document.querySelector('#submit-button').value = '👉 Hire a TC';
        }
        else if (ht == "data"){
            var $help = "Want a jumpstart with fresh data from the county? We are here to help!"
            document.querySelector('#data-description').style.fontWeight = "bold";
            document.querySelector('#submit-button').value = '👉 Request data';
        }
        else if (ht == "dialer"){
            var $help = "Want to focus on just making calls? We have data and a dialer available for you!"
            document.querySelector('#data-description').innerHTML = "This resource is focused on helping new wholesalers get their first couple of deals with a single-line dialer. We take care of the setup and compliance.";
            document.querySelector('#data-disclaimer').innerHTML = "*Note: Lanza Partners will pay for the data, the dialer seat and required setups. We keep track of usage metrics. If the dialer is unused, it will be reassigned to another applicant.";
            document.querySelector('#submit-button').value = '👉 Apply';
        }
        else if (ht == "zoom"){
            var $help = "Want to join our community and get specific questions answered?"
            document.querySelector('#submit-button').value = '👉 Join';
        }
        else {
            var $help = " "
        };
        document.querySelector('.h_type').innerHTML = $help;

        // Define existing contact welcome text
        $('#existing-text').toggleClass('existing--hide', need_name == 'Y');
        
        if (need_name == "N" & need_phone == "N" & need_company == "N"){
            var welcome_text = `<b>Welcome back, ${contact_name}!</b> We already have your contact info. <br>Let's jump to the details.`;
            document.querySelector('#existing-text').innerHTML = welcome_text;
        };
        if ((need_name == "N") && (need_phone == "Y" || need_company == "Y")){
            var welcome_text = `<b>Welcome back, ${contact_name}!</b> We just need a few extra contact details.`;
            document.querySelector('#existing-text').innerHTML = welcome_text;
        };
        // Pop fields
        document.querySelector("#address-text").innerHTML = `<b>Address:</b> ${address}.`;
        $("#email-2").val(email);
        $("#help_type").val(ht);
        $("#address-2").val(address);
        // Populate field
        $("#hid-2").val(hub_id);
        $("#zip").val(zip);
        // source id
        const sid = Cookies.get('sid');
        $("#v").val(sid);
        
        // Cookies
        if (email){
            Cookies.set('email', email, { expires: 300 });
        }
        if (contact_name){
            Cookies.set('fn', contact_name, { expires: 300 });
        }
        if (hub_id){
            Cookies.set('hid', hub_id, { expires: 300 });
        }
        // hide prel
        document.getElementById('preloader-submit2').style="display: none; opacity: 0";
    });

    // Define dealDispute link
    document.getElementById("deal-dispute").onclick = function () {
    location.href = "https://www.lanzapartners.com/deal-dispute?ht=" + ht + "&email=" + email + "&address=" + address;
    };

    // Define wrongAddress link
    document.getElementById("wrong-link").onclick = function () {
    location.href = "https://www.lanzapartners.com/submit?t=" + ht + "&email=" + email;
    };
});



// MLS fields
$(function() {
    const $select = $('#mls_status-2');
    const $d2a = $('#d2a');
    const $fields = $('#mlsdetails-div');
    const $inputPhone = $('#agent_phone-2');
    const $fields2 = $('#mlsdetails2-div');
    const $agentn = $('#agent-fn');
    const $agentl = $('#agent-ln');

    $select.on('change', (e) => {
        const value = e.currentTarget.value;

        if (value == 'on_market'){
            $fields.addClass('mlsdetails--show')
            $d2a.prop('required',true);
            // Unmark d2s fields as required
            $('#owners_name').prop('required',false);
            $('#owners_phone').prop('required',false);
            // Hide owners contact field
            $('#owners-div').removeClass('owners--show');

        } else {
            // Unmark d2a fields as required
            $d2a.prop('required',false);
            $inputPhone.prop('required',false);
            $agentn.prop('required',false);
            $agentl.prop('required',false);
            $fields.removeClass('mlsdetails--show');
            $fields2.removeClass('mlsdetails--show');

            // Optional to get seller contact fields
            $('#owners-div').addClass('owners--show');

            // Make it required if it's not dispo
            if (ht != "dispo"){
                console.log('making owners name required');
                $('#owners_name').prop('required',true);
                $('#owners_phone').prop('required',true);
            }
        }
    });
    
    $d2a.on('change', (e) => {
    	const value = e.currentTarget.value;
        if (value == 'yes'){
            $fields2.addClass('mlsdetails--show')
            $('#aphone').addClass('aphone--show');
            $inputPhone.prop('required',true);
            $agentn.prop('required',true);
            $agentl.prop('required',true);

            // Hide seller contact fields
            $('#owners-div').removeClass('owners--show');
            $('#owners_name').prop('required',false);
            $('#owners_phone').prop('required',false);

        } else {
            $inputPhone.prop('required',false);
            $agentn.prop('required',false);
            $agentl.prop('required',false);
            // Remove fields
            $('#aphone').removeClass('aphone--show');
            $fields2.removeClass('mlsdetails--show');

            // Optional to get seller contact fields
            $('#owners-div').addClass('owners--show');
            // Make it required if it's not dispo
            console.log("ht")
            console.log(ht)
            console.log('--')
            if (ht != "dispo"){
                console.log('making owners name required');
                $('#owners_name').prop('required',true);
                $('#owners_phone').prop('required',true);
            }
        }
    });
  });
