$(document).ready(function () {
    $("#add-user-form").submit(function (event) {
        event.preventDefault()
        var formData = new FormData(this);
        $.ajax({
            url : "/accounts/register/", // create institution
            type : "POST", // http method
            data : formData, // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                $("#error-username").html('')
                $("#error-password1").html('')
                $("#error-password2").html('')
                $("#error-first_name").html('')
                $("#error-limit").html('')
                $("#error-share_percentage").html('')
                res = JSON.parse(res)
                if (res.result == true){
                    window.location.reload();
                }
                else{
                    
                    for (const [key,value] of Object.entries(res)){

                    $("#error-"+key).html(value[0])
                  }
                }


                
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });

    })

    $("#edit-user").submit(function (event) {
        event.preventDefault()
        var formData = new FormData(this);
        $.ajax({
            url : "/accounts/edit/"+$("#edit-user #user_id").val()+"/", // create institution
            type : "POST", // http method
            data : formData, // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                res = JSON.parse(res)
                $("#edit-user #error-username").html('')
                $("#edit-user #error-first_name").html('')
                $("#edit-user #error-limit").html('')
                $("#edit-user #error-share_percentage").html('')
                if(res.result == true)
                {
                    window.location.reload();
                }
                else{
                    for (const [key,value] of Object.entries(res))
                    {
                        $("#edit-user #error-"+key).html(value)
                    }
                }    
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });

    })
    $("#change-password-form").submit(function(event){
        event.preventDefault()
        var formData = new FormData(this); 
        $.ajax({
            url : "/accounts/change_password/"+$("#change-password-form #user-id").val()+"/", // create institution
            type : "POST", // http method
            data : formData, // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                res = JSON.parse(res)
                $("#change-password-form #error-new_password1").html('')
                $("#change-password-form #error-new_password2").html('')
                
                if(res.result == true)
                {
                    window.location.reload();
                }
                else{
                    for (const [key,value] of Object.entries(res))
                    {
                        $("#change-password-form #error-"+key).html(value)
                    }
                }    
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });
    })
    $("#add-category-form").submit(function (event) {
        event.preventDefault()
        var formData = new FormData(this);
        $.ajax({
            url : "/panel/add-category/", // create institution
            type : "POST", // http method
            data : formData, // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                $("#error-name").html('')
                
                res = JSON.parse(res)
                console.log(res)
                if (res.result == true){
                    window.location.reload();
                }
                else{
                    
                    for (const [key,value] of Object.entries(res)){

                    $("#error-"+key).html(value[0])
                  }
                }


                
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });

    })

    $("#edit-category-form").submit(function (event) {
        event.preventDefault()
        var formData = new FormData(this);
        $.ajax({
            url : "/panel/edit-category/"+$("#edit-category-form #category_id").val()+"/", // create institution
            type : "POST", // http method
            data : formData, // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                res = JSON.parse(res)
                $("#edit-category-form #error-name").html('')
                if(res.result == true)
                {
                    window.location.reload();
                }
                else{
                    for (const [key,value] of Object.entries(res))
                    {
                        $("#edit-category-form #error-"+key).html(value)
                    }
                }    
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });

    })

    $("#add-request-form").submit(function (event) {
        event.preventDefault()
        var formData = new FormData(this);
        $.ajax({
            url : "/request/add-request/", // create institution
            type : "POST", // http method
            data : formData, // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                $("#add-request-form #error-category").html('')
                $("#add-request-form #error-users").html('')
                $("#add-request-form #error-start_at").html('')
                $("#add-request-form #error-amount").html('')
                $("#add-request-form #error-attachment").html('')
                $("#add-request-form #error-note").html('')
                res = JSON.parse(res)
                if (res.result == true){
                    window.location.reload();
                }
                else{
                    
                    for (const [key,value] of Object.entries(res)){
                        $("#add-request-form #error-"+key).html(value[0])
                    }
                } 
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });

    })

    $("#add-reversed-income-form").submit(function (event) {
        event.preventDefault()
        var formData = new FormData(this);
        $.ajax({
            url : "/request/add-reversed-income/", // create institution
            type : "POST", // http method
            data : formData, // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                $("#add-reversed-income-form #error-category").html('')
                $("#add-reversed-income-form #error-start_at").html('')
                $("#add-reversed-income-form #error-amount").html('')
                $("#add-reversed-income-form #error-attachment").html('')
                $("#add-reversed-income-form #error-note").html('')
                res = JSON.parse(res)
                if (res.result == true){
                    window.location.reload();
                }
                else{
                    
                    for (const [key,value] of Object.entries(res)){
                        $("#add-reversed-income-form #error-"+key).html(value[0])
                    }
                } 
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });

    })

    $("#add-reversed-to-available-form").submit(function (event) {
        event.preventDefault()
        var formData = new FormData(this);
        $.ajax({
            url : "/request/add-reversed-to-available/", // create institution
            type : "POST", // http method
            data : formData, // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                $("#add-reversed-to-available-form #error-category").html('')
                $("#add-reversed-to-available-form #error-start_at").html('')
                $("#add-reversed-to-available-form #error-amount").html('')
                $("#add-reversed-to-available-form #error-attachment").html('')
                $("#add-reversed-to-available-form #error-note").html('')
                res = JSON.parse(res)
                if (res.result == true){
                    window.location.reload();
                }
                else{
                    
                    for (const [key,value] of Object.entries(res)){
                        $("#add-reversed-to-available-form #error-"+key).html(value[0])
                    }
                } 
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });

    })
    $("#user-filter").change(function(){
        user = $(this).val()
        
        $.ajax({
            url : "/report/filter-user/"+user, // create institution
            // type : "GET", // http method
            data :'', // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                    res=JSON.parse(res)
                    var data = google.visualization.arrayToDataTable(
                        res.data
                        );
                        var options = {
                        chart: {
                            title: 'Report by the Category',
                            subtitle: 'Category details in this year.',
                        }     
                        };

                    var chart = new google.visualization.ColumnChart(
                        document.getElementById('chart_div'));

                    chart.draw(data, options);
                    
                
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });
    })
    $("#category-filter").change(function(){
        
        user = $(this).val()
        category = $(this).val()
        start = $("#start-filter").val()
        end = $("#end-filter").val()
        $.ajax({
            url : "/report/filter-category/"+category, // create institution
            // type : "GET", // http method
            data :'', // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                    res=JSON.parse(res)                
                    var data = google.visualization.arrayToDataTable(
                        res.data
                        );
                        var options = {
                        chart: {
                            title: 'Report by the Category',
                            subtitle: 'Category details in this year.',
                        }     
                        };

                    var chart = new google.visualization.ColumnChart(
                        document.getElementById('chart_div'));

                    chart.draw(data, options);
                    
                
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });
    })
    $("#start-filter").change(function(){
        user = $(this).val()
        category = $(this).val()
        start = $(this).val()
        end = $("#end-filter").val()
        $.ajax({
            url : "/report/filter-start/"+start, // create institution
            // type : "GET", // http method
            data :'', // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                    res=JSON.parse(res)
                    var data = google.visualization.arrayToDataTable(
                        res.data
                        );
                        var options = {
                        chart: {
                            title: 'Report by the Category',
                            subtitle: 'Category details in this year.',
                        }     
                        };

                    var chart = new google.visualization.ColumnChart(
                        document.getElementById('chart_div'));

                    chart.draw(data, options);
                    
                
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });
    })
    $("#end-filter").change(function(){
        user = $(this).val()
        category = $(this).val()
        start = $(this).val()
        end = $(this).val()
        $.ajax({
            url : "/report/filter-end/"+end, // create institution
            // type : "GET", // http method
            data :'', // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                    res=JSON.parse(res)
                    var data = google.visualization.arrayToDataTable(
                        res.data
                        );
                        var options = {
                        chart: {
                            title: 'Report by the Category',
                            subtitle: 'Category details in this year.',
                        }     
                        };

                    var chart = new google.visualization.ColumnChart(
                        document.getElementById('chart_div'));

                    chart.draw(data, options);
                    
                
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });
    })
    $("#edit-approve-list-form").submit(function(event){
        event.preventDefault()
        var formData = new FormData(this);
        $.ajax({
            url : "/request/edit-approve-list/"+$("#edit-approve-list-form #request_id").val()+"/", // create institution
            type : "POST", // http method
            data : formData, // data sent with the post request
            cache: false,
            contentType: false,
            processData: false,
            success : function(res) {
                $("#edit-approve-list-form #error-approve_list").html('')
                
                res = JSON.parse(res)
                if (res.result == true){
                    window.location.reload();
                }
                else{
                    
                    for (const [key,value] of Object.entries(res)){
                        $("#edit-approve-list-form #error-"+key).html(value[0])
                    }
                } 
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(err)
            }
        });
    })
})