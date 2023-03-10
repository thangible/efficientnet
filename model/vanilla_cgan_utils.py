from torch.autograd import Variable
import torch
import numpy as np

def discriminator_train_step(device, batch_size, discriminator, generator, d_optimizer, criterion, real_images, labels, class_num, z_size):
    
    # Init gradient 
    

    d_optimizer.zero_grad()
    # Disciminating real images
    real_validity = discriminator(real_images, labels)    
    # Calculating discrimination loss (real images)
    ones = Variable(torch.ones(real_validity.shape)).to(device)
    real_loss = criterion(real_validity, ones)    
    # Building z
    z = Variable(torch.randn(batch_size, z_size)).to(device)    
    # Building fake labels
    fake_labels = Variable(torch.LongTensor(np.random.randint(0, class_num, batch_size))).to(device)    
    # Generating fake images
    fake_images = generator(z, fake_labels)    
    # Disciminating fake images
    fake_validity = discriminator(fake_images, fake_labels)    
    # Calculating discrimination loss (fake images)
    zeros = Variable(torch.zeros(fake_validity.shape)).to(device)
    fake_loss = criterion(fake_validity, zeros )
    # Sum two losses
    d_loss = real_loss + fake_loss    
    # Backword propagation
    d_loss.backward()    
    # Optimizing discriminator
    d_optimizer.step()
    return d_loss.data

def generator_train_step(device, batch_size, discriminator, generator, g_optimizer, criterion, class_num, edge_labels, z_size):
    # Init gradient
    g_optimizer.zero_grad()    
    # Building z
    z = Variable(torch.randn(batch_size, z_size)).to(device)    
    # Building fake labels
    fake_labels = Variable(torch.LongTensor(np.random.choice(a = edge_labels, size = batch_size ))).to(device)  
    # fake_labels = Variable(torch.LongTensor(np.random.randint(0, class_num, batch_size))).to(device)    
    # Generating fake images
    fake_images = generator(z, fake_labels)    
    # Disciminating fake images
    validity = discriminator(fake_images, fake_labels)
    # Calculating discrimination loss (fake images)
    ones = Variable(torch.ones(validity.shape)).to(device)
    g_loss = criterion(validity, ones)
    # Backword propagation
    g_loss.backward()
    #  Optimizing generator
    g_optimizer.step()
    
    return g_loss.data