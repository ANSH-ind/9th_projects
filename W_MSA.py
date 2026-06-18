"""
*********************************************website: https://anshstudios.pages.dev/portfolio
*Coded by: ansh raj
*transformer name : swin attention 
*total function: 2 (window_reverse,window_pertation)
*class: 1 (window attention)
*******************************************
"""


def window_pertation(x,window_size):
    """
    input must be [B,H,W,C]
    output: [B*nW,window_size,window_size,C]
    """
    B,H,W,C = x.shape
    x = x.reshape(B,W//window_size,window_size,H//window_size,window_size,C).permute(0,1,3,2,4,5).contiguous().view(-1,window_size,window_size,C)
    return x
    
def window_reverse(x,window_size,H,W):
    """
    input must be [B*nW,N,N,C]
    output : [B,H,W,C]
    """
    B = int(x.shape[0]/(H*W/window_shape/window_shape))
    reversed_w = x.view(B,H//window_shape,window_shape,W//window_shape,window_shape,C)
    reversed_w = reversed_w.permute(0,1,3,2,4,5).contiguous().view(B,H,W,-1)
    return reversed_w
    
class W_MSA(nn.Module):
    def __init__(self,embed_dim,num_head,window_size,atten_drop= 0.2 ,qkv_bias=True):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_head = num_head
        self.window_size = window_size
        self.atten_drop = atten_drop
        self.head_dim = embed_dim//num_head
        self.scale = head_dim**-0.5
        self.qkv_bias = qkv_bias
        
        self.relative_position_bias_table = nn.permute(torch.zeros((2*window_size-1*2*window_size-1),num_head))
        
        coords_h = torch.arange(window_size)
        coords_w = torch.arange(window_size)
        coords = torch.stack(torch.meshgrid([coords_h,coords_w],indexing="ij"))#create coordinates like (x,y) and stack them so that is can be 2,Wh,Ww
        
        flatten_coords = torch.flatten(coords,1) #flatten it to make like this shape 2,N there N is Wh*Ww
        relative_coords = flatten_coords[:,:,None]-[:,None,:] # shape 2,N,N
        relative_coords = relative_coords.permute(1,2,0)
        #convert all negatives index to postive because python dosen't support negative indexing 
        
        realtive_coords[:,:,0] += window_size-1
        relative_coords[:,:,1] += window_size-1
        relative_coords[:,:,0] *= 2*window_size-1
        self.relative_position_index = realtive_coords.sum(-1)
        
        self.register_buffer("relative_position_index",relative_position_index)
        
        self.qkv = nn.Linear(embed_dim,embed_dim*3,bias = self.qkv_bias)
        self.attendrop = nn.Dropout(self.atten_drop)
        self.proj = nn.Linear(dim*3,dim)
        self.proj_drop = nn.Dropout(0.1)
        self.Softmax = nn.softmax(dim=-1)
        
        def forward(self,x, mask=None):
            """
            input: [B*nW,N,C]
            output: [B*nW,N,C]
            """
            B_,N,C = x shape
            qkv = self.qkv(x).reshape(B_,N,3,self.num_head,self.embed_dim//self.num_head).permute(2,0,3,1,4).contiguous()
            Q,K,V = qkv[0], qkv[1], qkv[2]
            
            #each token included [B,nH,N,C]
            Q = Q*self.scale
            atten = (Q@k.transpose(-2,-1))
            
            bias = self.relative_position_bias_table[self.relative_position_index.view(-1)].view(window_size*window_size,window_size*window_size,-1)
            
            atten = atten+bias.unsqueeze(dim=0)
            
            if self.mask is not None:
                nW = mask.shape[0]
                atten = atten.view(B_//nW,nW,self.num_head,N,N)+mask.unsqueeze(1).unsqueeze(2)
                atten = atten.view(-1,self.num_head,N,N)
             
            atten = self.Softmax(atten)
            atten = self.atten_drop(atten)
            
            atten = (atten@v).transpose(1,2)
            atten = self.proj(atten)
            atten = self.proj_drop(atten)
            
            return atten
