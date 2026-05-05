n = 0
mean = 0.
M2 = 0.

#define our function in which all required functions are run through loop
def find_mean_std(data_loader):
  for images,_ in data_loader:
    images = images.view(images.size(0),images.size(1),-1)
    images = images.permute(1,0,2).contiguous().views(images.size(1),-1)
    
    batch_pixels = images.size(1)
    n_new = batch_pixels+n
    
    batch_mean = images.mean(dim=1)
    batch_var = images.var(dim=1, unbiased=False)
    
    delta = batch_mean-mean
    
    mean = mean+delta*batch_pixels/n_new
    
    M2 = M2+batch_var*batch_pixels*(delta**2)*n*batch_pixels/n_new
    
    n = n_new
    
  variance = M2/n
  std = torch.sqrt(variance)
  return mean,std
