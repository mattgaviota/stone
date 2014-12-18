<?= form_open('index.php/home/recordando_clave', array('class'=>'form-horizontal jumbotron')); ?>
	<legend>Para obtener una nueva clave ingrese su usuario y su dirección de correo</legend>

	<?= my_validation_errors(validation_errors()); ?>

	<div class="row">
		<div class="form-group">
			<?= form_label('Usuario: ', 'dni', array('class'=>'col-md-4 control-label')); ?>
			<div class="col-md-5">
				<?= form_input(array('class'=>'form-control','type'=>'text', 'name'=>'dni', 'id'=>'dni', 'placeholder'=>'Tu usuario (DNI)', 'value'=>set_value('dni'))); ?>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Email: ', 'email', array('class'=>'col-md-4 control-label')); ?>
			<div class="col-md-5">
				<?= form_input(array('class'=>'form-control','type'=>'text', 'name'=>'email', 'id'=>'email', 'placeholder'=>'Tu email', 'value'=>set_value('email'))); ?>
			</div>
		</div>
	</div>

	<hr>

	<div class="row">
		<div class="form-group">
			<div class="col-md-offset-3">
				<div class="col-md-8 col-xs-12">
					<?= form_button(array('type'=>'submit', 'content'=>' Confirmar', 'class'=>'btn btn-success glyphicon glyphicon-ok')); ?>
			
					<?= anchor('home/ingreso', ' Cancelar',array('class'=>'btn btn-default glyphicon glyphicon-remove')); ?>
				</div>	
			</div>
		</div>
	</div>
<?= form_close(); ?>