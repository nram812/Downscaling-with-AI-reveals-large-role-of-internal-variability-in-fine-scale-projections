import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import tensorflow
import xarray as xr
from dask.diagnostics import ProgressBar
from tensorflow.keras.callbacks import Callback
import tensorflow.keras.backend as K
import numpy as np
import pandas as pd
import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.colors as mcolors

class GeneratorCheckpoint(Callback):
    def __init__(self, generator, filepath, period):
        super().__init__()
        self.generator = generator
        self.filepath = filepath
        self.period = period

    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % self.period == 0:
            self.generator.save(f"{self.filepath}_epoch_{epoch + 1}.h5")


class DiscriminatorCheckpoint(Callback):
    def __init__(self, discriminator, filepath, period):
        super().__init__()
        self.discriminator = discriminator
        self.filepath = filepath
        self.period = period

    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % self.period == 0:
            self.discriminator.save(f"{self.filepath}_epoch_{epoch + 1}.h5")


def discriminator_loss(real_img, fake_img):
    real_loss = tf.reduce_mean(real_img)
    fake_loss = tf.reduce_mean(fake_img)
    return fake_loss - real_loss


class PredictionCallback(tf.keras.callbacks.Callback):
    def __init__(self, unet, generator, wgan_object,x_input, y_input, save_dir=None, batch_size =30, orog =None,
                                             output_mean =None, output_std = None, varname = "pr"):
        """
        Args:
            model: The trained model.
            sample_input: A sample input tensor to generate predictions.
            save_dir: Directory where prediction images will be saved.
        """
        super(PredictionCallback, self).__init__()
        self.unet = unet
        self.generator = generator
        self.wgan = wgan_object
        self.x_input = x_input
        self.y_input = y_input
        self.save_dir = save_dir
        self.batch_size =batch_size
        self.orog = orog
        self.output_mean = output_mean
        self.output_std = output_std
        self.varname = varname

        
        os.makedirs(save_dir, exist_ok=True)

    def on_epoch_end(self, epoch, logs=None):
        """Runs at the end of each epoch to save a prediction image."""
        # Generate prediction
        if epoch % 3 == 0:
            tf.random.set_seed(16)
            random_latent_vectors = tf.random.normal(
                shape=(self.batch_size,) + self.wgan.latent_dim[0]
            )
            random_latent_vectors1 = tf.random.normal(
                shape=(self.batch_size,) + self.wgan.latent_dim[1]
            )
            orog_vector = self.wgan.expand_conditional_inputs(self.orog, self.batch_size)
            #average_combined, orog_vector,time_of_year_combined, spatial_means_combined,
            #                 spatial_stds_combined
            unet_prediction = self.unet.predict([
                                          self.x_input[0].values[:self.batch_size], orog_vector[:self.batch_size]], verbose=0)

            gan_prediction = self.generator.predict([random_latent_vectors,random_latent_vectors1,
                                          self.x_input[0], orog_vector,unet_prediction])

            if self.varname == "pr":

                unet_final = tf.math.exp(unet_prediction) -1
                gan_final = tf.math.exp(unet_prediction + gan_prediction)-1
            else:
                unet_final = tf.squeeze(unet_prediction) * self.output_std + self.output_mean
                gan_final = tf.squeeze(unet_prediction + gan_prediction) * self.output_std + self.output_mean

            y_copy = self.y_input.copy()
            y_2 = self.y_input.copy()
            y_copy.values = tf.squeeze(unet_final)
            y_2.values = tf.squeeze(gan_final)
            y_2 = y_2.where(y_2>0.5, 0.0)
            y_copy = y_copy.where(y_2>0.5, 0.0)
            boundaries2 = [0, 5,12.5, 15, 20, 25,30, 35, 40, 50, 60, 70, 80, 100, 125, 150, 200, 250]
            colors2 = [[0.000, 0.000, 0.000, 0.000], [0.875, 0.875, 0.875, 0.784],\
                      [0.761, 0.761, 0.761, 1.000], [0.639, 0.886, 0.871, 1.000], [0.388, 0.773, 0.616, 1.000],\
                      [0.000, 0.392, 0.392, 0.588], [0.000, 0.576, 0.576, 0.667], [0.000, 0.792, 0.792, 0.745],\
                      [0.000, 0.855, 0.855, 0.863], [0.212, 1.000, 1.000, 1.000], [0.953, 0.855, 0.992, 1.000],\
                      [0.918, 0.765, 0.992, 1.000], [0.918, 0.612, 1.000, 1.000], [0.878, 0.431, 1.000, 1.000],\
                      [0.886, 0.349, 1.000, 1.000], [0.651, 0.004, 0.788, 1.000], [0.357, 0.008, 0.431, 1.000],\
                      [0.180, 0.000, 0.224, 1.000]]
            #reviated for clarity

            # Create the colormap using ListedColormap
            cmap = mcolors.ListedColormap(colors2)
            norm = mcolors.BoundaryNorm(boundaries2, cmap.N)

            for i in range(8):
                print(i)
                fig, ax = plt.subplots(1, 3, figsize = (16, 6), subplot_kw = dict(projection = ccrs.PlateCarree(central_longitude =171.77)))
                if self.varname =="pr":
                    y_copy.isel(time =i).plot(ax = ax[0], transform = ccrs.PlateCarree(),cmap= 'viridis')
                    y_2.isel(time =i).plot(ax = ax[1], transform = ccrs.PlateCarree(), cmap = 'viridis')
                    (np.exp(self.y_input.isel(time =i))-1) .plot(ax = ax[2], transform = ccrs.PlateCarree(), cmap='viridis')
                else:
                    true = self.y_input.isel(time =i) * self.output_std + self.output_mean
                    min_t = true.values.min()
                    max_t = true.values.max()
                    levels = np.arange(min_t, max_t, 0.5)
                    y_copy.isel(time =i).plot(ax = ax[0], transform = ccrs.PlateCarree(), cmap ='RdBu_r', levels = levels)
                    y_2.isel(time =i).plot(ax = ax[1], transform = ccrs.PlateCarree(), cmap ='RdBu_r', levels = levels)
                    true.plot.contourf(ax = ax[2], transform = ccrs.PlateCarree(), cmap ='RdBu_r', levels = levels)
                ax[0].coastlines('10m')
                ax[1].coastlines('10m')
                ax[2].coastlines('10m')
                ax[0].set_title('Unet')
                ax[1].set_title('GAN')
                ax[2].set_title('GT')
                # Save the figure
                filename = os.path.join(self.save_dir, f"epoch_{epoch+1}_{i}.png")
                plt.savefig(filename, bbox_inches="tight", dpi =200)
                plt.close()

            print(f"Saved prediction image to {filename}")


def generator_loss(fake_img):
    return -tf.reduce_mean(fake_img)


class WGAN_Cascaded_IP(keras.Model):
    """
    A residual GAN to downscale precipitatoin, this GAN incorparates an Intensity Constraint
    """

    def __init__(self, discriminator, generator, latent_dim,
                 discriminator_extra_steps=3, gp_weight=10.0, ad_loss_factor=1e-3,
                 latent_loss=5e-2, orog=None, he=None,
                 vegt=None, unet=None, train_unet=True, intensity_weight = 1, average_intensity_weight =0.0, varname = "pr"):
        super(WGAN_Cascaded_IP, self).__init__()

        self.discriminator = discriminator
        self.generator = generator
        self.latent_dim = latent_dim
        self.d_steps = discriminator_extra_steps
        self.gp_weight = gp_weight
        self.ad_loss_factor = ad_loss_factor
        self.latent_loss = latent_loss
        self.orog = orog
        self.he = he
        self.vegt = vegt
        self.unet = unet
        self.train_unet = train_unet
        self.intensity_weight = intensity_weight
        self.average_itensity_weight = average_intensity_weight
        self.varname = varname

    def compile(self, d_optimizer, g_optimizer, d_loss_fn,
                g_loss_fn, u_loss_fn, u_optimizer):
        super(WGAN_Cascaded_IP, self).compile()
        self.d_optimizer = d_optimizer
        self.g_optimizer = g_optimizer
        self.d_loss_fn = d_loss_fn
        self.g_loss_fn = g_loss_fn
        self.u_loss_fn = u_loss_fn
        self.u_optimizer = u_optimizer

    def gradient_penalty(self, batch_size, real_images, fake_images, average, orog_vector, he_vector, vegt_vector,
                         unet_preds):
        """
        need to modify
        """
        # Get the interpolated image
        alpha = tf.random.normal([batch_size, 1, 1, 1], 0.0, 1.0)
        diff = fake_images - real_images
        interpolated = real_images + alpha * diff

        with tf.GradientTape() as gp_tape:
            gp_tape.watch(interpolated)
            pred = self.discriminator([interpolated, average, orog_vector, unet_preds],
                                      training=True)

        grads = gp_tape.gradient(pred, [interpolated])[0]
        norm = tf.sqrt(tf.reduce_sum(tf.square(grads), axis=[1, 2, 3]))
        gp = tf.reduce_mean((norm - 1.0) ** 2)
        return gp

    @staticmethod
    def expand_conditional_inputs(X, batch_size):
        expanded_image = tf.expand_dims(X, axis=0)  # Shape: (1, 172, 179)

        # Repeat the image to match the desired batch size
        expanded_image = tf.repeat(expanded_image, repeats=batch_size, axis=0)  # Shape: (batch_size, 172, 179)

        # Create a new axis (1) on the last axis
        expanded_image = tf.expand_dims(expanded_image, axis=-1)
        return expanded_image
    @staticmethod
    def process_real_images(real_images_obj):
        output_vars, averages = real_images_obj  # Unpack the input

        # Extract relevant variables from the output_vars dictionary
        real_images = [
            output_vars['pr']
        ]

        real_images_future = [
            output_vars['pr_future'],
            
        ]

        # Extract average and average_future
        average = averages["X"]
        average_future = averages["X_future"]

        # Combine variables into single tensors
        real_images = tf.concat([tf.expand_dims(img, axis=-1) for img in real_images], axis=-1)
        real_images_future = tf.concat([tf.expand_dims(img, axis=-1) for img in real_images_future], axis=-1)

        # Combine all GCMs into one single batch timestep
        real_images = tf.concat([real_images[:, :, :, i, :] for i in range(real_images.shape[3])], axis=0)
        real_images_future = tf.concat([real_images_future[:, :, :, i, :] for i in range(real_images_future.shape[3])],
                                       axis=0)
        average = tf.concat([average[:, :, :, i, :] for i in range(average.shape[3])], axis=0)
        average_future = tf.concat([average_future[:, :, :, i, :] for i in range(average_future.shape[3])], axis=0)
        
        average_combined = tf.concat([average, average_future], axis =0)
        real_images_combined = tf.concat([real_images, real_images_future], axis =0)
        return real_images_combined, average_combined

    def train_step(self, real_images):
        real_images, average = self.process_real_images(real_images)

            # here the average represents the conditional input

        batch_size = tf.shape(real_images)[0]
        orog_vector = self.expand_conditional_inputs(self.orog, batch_size)
        he_vector = self.expand_conditional_inputs(self.he, batch_size)
        vegt_vector = self.expand_conditional_inputs(self.vegt, batch_size)
        # make sure the auxiliary inputs are the same shape as the training batch
        # if the U-Net is trained, apply gradients otherwise only use inference mode from the U-Net
        if self.train_unet:
            with tf.GradientTape() as tape:
                random_latent_vectors = tf.random.normal(
                    shape=(batch_size,) + self.latent_dim[0]
                )

                init_prediction = self.unet([average,
                                             orog_vector], training=True)
                orog_vec_mask = tf.cast(tf.squeeze(orog_vector) > 0.001, 'float32')
                loss_rain_ocean_unet = self.u_loss_fn(tf.squeeze((real_images[:, :, :, 0:1])) * (1 - orog_vec_mask), tf.squeeze(init_prediction) * (1 - orog_vec_mask))

                loss_rain_land_unet = self.u_loss_fn(tf.squeeze((real_images[:, :, :, 0:1])) * orog_vec_mask, tf.squeeze(init_prediction) * orog_vec_mask)

                loss_rain_unet = (5* loss_rain_land_unet + loss_rain_ocean_unet)/6.0
                mae_unet = loss_rain_unet#self.u_loss_fn(real_images[:, :, :], init_prediction)
            u_gradient = tape.gradient(mae_unet, self.unet.trainable_variables)
            # Update the weights of the generator using the generator optimizer
            self.u_optimizer.apply_gradients(zip(u_gradient, self.unet.trainable_variables))
        else:
            with tf.GradientTape() as tape:
                random_latent_vectors = tf.random.normal(
                    shape=(batch_size,) + self.latent_dim[0]
                )

                init_prediction = self.unet([ average,
                                             orog_vector], training=True)
                mae_unet = self.u_loss_fn(real_images[:, :, :], init_prediction)
        # loop through the discriminator steps
        for i in range(self.d_steps):
            # Get the latent vector
            random_latent_vectors = tf.random.normal(
                shape=(batch_size,) + self.latent_dim[0]
            )
            random_latent_vectors1 = tf.random.normal(
                shape=(batch_size,) + self.latent_dim[1]
            )

            with tf.GradientTape() as tape:

                init_prediction_unet = self.unet([ average,
                                                  orog_vector], training=True)
                # compute ground truth residuals
                residual_gt = (real_images - init_prediction_unet)
                init_prediction = init_prediction_unet
                # crete fake residuals (these are residual by default)
                fake_images = self.generator([random_latent_vectors,random_latent_vectors1, average,
                                              orog_vector, init_prediction], training=True)

                fake_logits = self.discriminator(
                    [fake_images, average, orog_vector, init_prediction], training=True)
                # Get the logits for the real images
                real_logits = self.discriminator(
                    [residual_gt, average, orog_vector, init_prediction], training=True)

                # Calculate the discriminator loss using the fake and real image logits
                d_cost = self.d_loss_fn(real_img=real_logits, fake_img=fake_logits)
                # Calculate the gradient penalty
                gp = self.gradient_penalty(batch_size, residual_gt, fake_images, average, orog_vector, he_vector,
                                           vegt_vector, init_prediction)

                # Add the gradient penalty to the original discriminator loss
                d_loss = d_cost + gp * self.gp_weight  # + #50 * tf.keras.losses.mean_squared_error(average, fake_image_average)

            # Get the gradients w.r.t the discriminator loss
            d_gradient = tape.gradient(d_loss, self.discriminator.trainable_variables)
            # Update the weights of the discriminator using the discriminator optimizer
            self.d_optimizer.apply_gradients(zip(d_gradient, self.discriminator.trainable_variables))

        # Train the generator
        random_latent_vectors = tf.random.normal(
            shape=(8,) + (batch_size,) + self.latent_dim[0]
        )
        random_latent_vectors1 = tf.random.normal(
            shape=(8,) + (batch_size,) + self.latent_dim[1]
        )
        # Generator steps
        with tf.GradientTape() as tape:
            # Generate fake images using the generator
            init_prediction_unet = self.unet([average,
                                              orog_vector], training=True)

            init_prediction = init_prediction_unet  # (init_prediction_unet - min_value)/(max_value - min_value)
            # compute ground truth residuals
            residual_gt = (real_images - init_prediction_unet)
            # creatinging an ensemble
            generated_images_v2 = [tf.expand_dims(self.generator(
                [random_latent_vectors[i],random_latent_vectors1[i], average, orog_vector, init_prediction],
                training=True), axis =0) for i in range(2)]
            generated_images_v1 = generated_images_v2[0][0]
            # an ensemble mean across 8-members
            generated_images_v2 = generated_images_v1#tf.math.reduce_mean(tf.concat(generated_images_v2, axis =0), axis =0)

            generated_images = generated_images_v1  # tf.math.exp(generated_images_v1[:,:,:,0] +
            # residual predictions from the GAN

            gen_img_logits = self.discriminator(
                [generated_images, average, orog_vector, init_prediction], training=True)
            # compute the content loss or the MSE, this is the errors in the residuals
            #mae = tf.keras.losses.mean_squared_error(residual_gt, generated_images_v2)
            orog_vec_mask = tf.cast(tf.squeeze(orog_vector) > 0.001, 'float32')
            loss_rain_ocean_gan = self.u_loss_fn(tf.squeeze((residual_gt)) * (1 - orog_vec_mask), tf.squeeze(generated_images_v2) * (1 - orog_vec_mask))

            loss_rain_land_gan = self.u_loss_fn(tf.squeeze((residual_gt)) * orog_vec_mask, tf.squeeze(generated_images_v2) * orog_vec_mask)

            mae = (5* loss_rain_land_gan + loss_rain_ocean_gan)/6.0
            
            
            # compute the "true" error.
            gan_mae = tf.keras.losses.mean_squared_error(residual_gt, generated_images_v2)

            # compute the intensity on the batch across each individual timestep (not the 0th dimension)
            gamma_loss_func = mae
            if self.varname == "pr":
                maximum_intensity = tf.nn.max_pool2d(real_images, ksize=(20,20), strides=10, padding="SAME")#tf.math.reduce_max(
                #    real_images, axis=[0,-1])
                maximum_intensity_predicted = tf.nn.max_pool2d(generated_images_v1 + init_prediction_unet,
                                                               ksize=(20,20), strides=10, padding="SAME")
                #tf.math.reduce_max(generated_images_v1 + init_prediction_unet,
                 #                                                                axis=[0,-1])
                
                # New contraint here
                # Max precipitation from GAN and U-Net
                # Max precipitation from GAN and U-Net
                #                 condition = tf.logical_and(generated_images_v1 > 4.0, init_prediction_unet < 1.25)
                #                 # Apply penalty only where condition is True
                #                 excess = tf.where(condition,
                #                                   generated_images_v1 - 3.0,  # You can adjust to -4.0 if you want to penalize GAN > 4 more harshly
                #                                   tf.zeros_like(generated_images_v1))

                #                 # Example: squared penalty
                #                 penalty = tf.reduce_mean(tf.square(excess))
                #                 penalty_weight = 5.5  # Set this based on your experiment
                            
                
                maximum_intensity_error = tf.reduce_mean(
                tf.abs(maximum_intensity - maximum_intensity_predicted) ** 2)# + penalty * penalty_weight
                average_intensity = tf.math.reduce_mean(
                real_images, axis=[-1, -4])
                average_intensity_predicted = tf.math.reduce_mean(generated_images_v1 + init_prediction_unet,
                                                              axis=[-1, -4])

                average_intensity_error = tf.reduce_mean(
               tf.abs(average_intensity - average_intensity_predicted) ** 2)
            else:
                maximum_intensity = tf.math.reduce_max(
                    real_images, axis=[-1, -2, -3])
                maximum_intensity_predicted = tf.math.reduce_max(generated_images_v1 + init_prediction_unet,
                                                                 axis=[-1, -2, -3])
                maximum_intensity_error = tf.reduce_mean(
                tf.abs(maximum_intensity - maximum_intensity_predicted) ** 2)
                minimum_intensity = tf.math.reduce_min(
                    real_images, axis=[-1, -2, -3])
                minimum_intensity_predicted = tf.math.reduce_min(generated_images_v1 + init_prediction_unet,
                                                                 axis=[-1, -2, -3])
                minimum_intensity_error = tf.reduce_mean(
                tf.abs(minimum_intensity - minimum_intensity_predicted) ** 2)
                maximum_intensity_error = 1/2 * (minimum_intensity_error + maximum_intensity_error)
                average_intensity = tf.math.reduce_mean(
                real_images, axis=[-1, -4])
                average_intensity_predicted = tf.math.reduce_mean(generated_images_v1 + init_prediction_unet,
                                                              axis=[-1, -4])

                average_intensity_error = tf.reduce_mean(
               tf.abs(average_intensity - average_intensity_predicted) ** 2)
                
#             maximum_intensity_error = tf.reduce_mean(
#                 tf.abs(maximum_intensity - maximum_intensity_predicted) ** 2)
            adv_loss = self.ad_loss_factor * self.g_loss_fn(gen_img_logits)
            # Calculate the generator loss
            g_loss = adv_loss + gamma_loss_func + self.average_itensity_weight * average_intensity_error + self.intensity_weight * maximum_intensity_error ## + self.latent_loss * latent_loss
        # + tf.reduce_mean(
        #     tf.abs(average_intensity - average_intensity_predicted)) ** 2
        # Get the gradients w.r.t the generator loss
        gen_gradient = tape.gradient(g_loss, self.generator.trainable_variables)
        # Update the weights of the generator using the generator optimizer
        self.g_optimizer.apply_gradients(zip(gen_gradient, self.generator.trainable_variables))

        return {"d_loss": d_loss, "g_loss": g_loss, "residual_loss": gamma_loss_func, "adv_loss": adv_loss,
                "unet_loss": mae_unet, "gan_mae": mae, "max_iten_pred": tf.math.exp(maximum_intensity_predicted), "max_iten_true": tf.math.exp(maximum_intensity)}


