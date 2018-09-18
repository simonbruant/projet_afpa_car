<template>
<div id="calendar_app" class='card'>
	<div id="datepicker">
		<div id="titre_calendar" class="card-header bg-success">Votre calendrier</div>
		<div class="card-content">
			<div class="row">
				<div class="col-md-6" id="conteneur_calendrier">
					<div id="date_picker_css" class="mt-3 mb-3">
						<div class="example">
							<datepicker 
							:inline="true"
							:monday-first="true" 
							:full-month-name="true" 
							calendar-class="datepicker_calendar"
							:language="fr"
							:format="customFormatter">
							</datepicker>
						</div>
					</div>
				</div>
				<div class="col-md-6 mt-3">
					<p>{{ message }} </p>
				</div>
			</div>
		</div>
	</div>
</div>
</template>

<script>

import Datepicker from 'vuejs-datepicker';
import {fr} from '../../node_modules/vuejs-datepicker/dist/locale'
import moment from 'moment'


export default {
	name: "calendar_app",
	components: {
		Datepicker 	
	},
	data() {
		return {
		fr: fr,
		message : '',
		
		};
	},
	methods: {
        // dateSelected :function(e){
        //     console.log (e),
        //     this.message = e
        // },
        customFormatter(date) {
            this.message =  moment(date).format('D MMMM YYYY');
            console.log(this.message)
        }
    }
}

</script>
