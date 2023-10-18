from models import RotationalVariationalAutoencoder

def test_rotational_variational_autoencoder():

    z_dim = 2
    model = RotationalVariationalAutoencoder(z_dim=z_dim)
    input = model.example_input_array
    batch_size = input.shape[0]

    (z_mean, z_var), (_, _), _, recon = model(input)

    assert z_mean.shape == (batch_size, z_dim)
    assert z_var.shape == (batch_size, z_dim)
    assert recon.shape == input.shape