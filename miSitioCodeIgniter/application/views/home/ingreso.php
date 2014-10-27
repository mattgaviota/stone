<?= form_open('index.php/home/ingresar', array('class'=>'form-horizontal jumbotron')); ?>
	<legend>Ingreso al sistema</legend>

	<?= my_validation_errors(validation_errors()); ?>
	<?= my_mensaje_confirmacion($mostrar)?>

	<div class="row">
		<div class="form-group">
			<?= form_label('Usuario: ', 'dni', array('class'=>'col-md-2 control-label')); ?>
			<div class="col-md-3">
				<?= form_input(array('class'=>'form-control','type'=>'text', 'name'=>'dni', 'id'=>'dni', 'placeholder'=>'Tu usuario (DNI)', 'value'=>set_value('dni'))); ?>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Password: ', 'label_password', array('class'=>'col-md-2 control-label')); ?>
			<div class="col-md-3">
				<?= form_input(array('class'=>'form-control','type'=>'password', 'name'=>'password', 'id'=>'password', 'placeholder'=>'Tu password', 'value'=>set_value('password'))); ?>
			</div>	
		</div>
	</div>

	<hr>

	<div class="row">
		<div class="form-group">
			<div class="col-md-offset-1">
				<div class="col-md-6 col-xs-9">
					<?= form_button(array('type'=>'submit', 'content'=>' Ingresar', 'class'=>'btn btn-primary glyphicon glyphicon-arrow-right')); ?>
			
					<?= anchor('home/index', ' Cancelar',array('class'=>'btn btn-default glyphicon glyphicon-remove')); ?>
				</div>	
			</div>
		</div>
	</div>
	

<?= form_close(); ?>